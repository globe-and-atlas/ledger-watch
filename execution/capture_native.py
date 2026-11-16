"""Capture fixture Hi-Fi from the already-owned Emery emulator."""
from pathlib import Path
import argparse
import json
import socket
import subprocess
import time
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
PALETTES=[(0xFFFFFF,0,0xAA0000),(0xFFFFAA,0,0xAA0000),(0,0xFFFFFF,0xFF5500),(0xAAFFAA,0x005500,0x005500),(0xAAFFFF,0x000055,0x0055AA),(0x000055,0xFFFFFF,0x55FFFF),(0x000055,0xFFFFFF,0xFF55AA)]

def rgb(value):
    return ((value>>16)&255,(value>>8)&255,value&255)

def screenshot(port, peak=255):
    path=ROOT/'.tmp/native.ppm'
    path.unlink(missing_ok=True)
    with socket.create_connection(('localhost',port),timeout=5) as connection:
        connection.recv(65536)
        connection.sendall(f'screendump "{path.resolve()}"\n'.encode())
        deadline=time.monotonic()+5
        while time.monotonic()<deadline:
            connection.recv(65536)
            try:
                image=Image.open(path).convert('RGB');break
            except (FileNotFoundError,OSError):continue
        else:raise TimeoutError('Incomplete QEMU screendump')
    actual=max(max(pixel) for pixel in image.get_flattened_data())
    image=image.point(lambda channel:round(channel/max(actual,1)*peak/85)*85)
    path.unlink(missing_ok=True)
    assert image.size==(200,228)
    return image

import importlib.util
_spec=importlib.util.spec_from_file_location('ledger_fonts',ROOT/'execution/generate_fonts.py')
fonts=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(fonts)


def text_width(text):return sum(fonts.label_mask(c)[1]+1 for c in text)-1 if text else 0

def expected_text(text,x,width,fg,bg):
    image=Image.new('RGB',(width,24),bg)
    for char in text:
        mask,w=fonts.label_mask(char);image.paste(fg,(x,0,x+32,20),mask);x+=w+1
    return image


def check(image,hour,minute,fmt,date,palette,battery):
    bg,fg,accent=map(rgb,PALETTES[palette]);display=hour if fmt==2 else hour%12 or 12
    values=[display//10,display%10,minute//10,minute%10];positions=[14,53,111,150]
    left=min([96]+[x+fonts.digit_mask(n).getbbox()[0] for n,x in zip(values,positions)])
    right=max([102]+[x+fonts.digit_mask(n).getbbox()[2]-1 for n,x in zip(values,positions)])
    offset=int((199-left-right)/2)
    for n,x in zip(values,positions):
        expected=Image.new('RGB',(36,64),bg);expected.paste(fg,(0,0),fonts.digit_mask(n).crop((0,0,36,64)))
        assert image.crop((x+offset,54,x+offset+36,118)).tobytes()==expected.tobytes(),'Serif numeral pixels differ'
    ink=[x for y in range(54,118) for x in range(200) if image.getpixel((x,y))==fg]
    assert abs((min(ink)+max(ink))/2-99.5)<=.5,'Clock ink off center'
    ampm=('PM' if hour>=12 else 'AM') if fmt==1 else ''
    expected=expected_text(ampm,(200-text_width(ampm))//2,200,fg,bg)
    assert image.crop((0,28,200,52)).tobytes()==expected.tobytes(),'AMPM differs'
    dates=['','THU NOV 05','2026-11-05','11/05/2026','05/11/2026'];text=dates[date]
    expected=expected_text(text,(200-text_width(text))//2,200,fg,bg)
    assert image.crop((0,145,200,169)).tobytes()==expected.tobytes(),'Date pixels differ'
    expected=expected_text('BATTERY',13,200,fg,bg);percent=f'{battery}%';x=187-text_width(percent)
    for char in percent:
        mask,w=fonts.label_mask(char);expected.paste(accent,(x,0,x+32,20),mask);x+=w+1
    assert image.crop((0,194,200,218)).tobytes()==expected.tobytes(),'Battery label differs'
    assert image.getpixel((13,20))==accent,'Accent rule differs'
    assert image.getpixel((13,132))==fg,'Rule differs'
    return {'clock_midpoint':(min(ink)+max(ink))/2,'exact_glyph_pixels':True}


def send(keys,uuid,values):
    result=subprocess.run(['pebble','send-app-message','--emulator','emery','--app-uuid',uuid,'--int']+[f'{keys.get(k,k)}={v}' for k,v in values.items()],cwd=ROOT/'watchface',capture_output=True,text=True,timeout=45)
    if result.returncode:raise RuntimeError(result.stderr[-1500:])


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--monitor',type=int,required=True);options=parser.parse_args()
    keys=json.loads((ROOT/'watchface/build/js/message_keys.json').read_text());uuid=json.loads((ROOT/'watchface/package.json').read_text())['pebble']['uuid']
    cases=[('default',10,8,2,1,0,82)]
    cases += [(f'palette-{p}',10,8,2,1,p,82) for p in range(6)]
    cases += [('custom',10,8,2,1,6,82)]
    cases += [(f'date-{d}',10,8,2,d,0,82) for d in range(5)]
    cases += [(f'{name}-{fmt}h',h,m,fmt,1,0,82) for name,h,m in [('midnight',0,0),('noon',12,0),('late',23,59),('eleven',11,11),('fourteen',14,44)] for fmt in [1,2]]
    cases += [('battery-empty',10,8,2,1,0,0),('battery-full',10,8,2,1,0,100)]
    evidence=[]
    for name,h,m,fmt,date,palette,battery in cases:
        send(keys,uuid,{'Palette':palette,'TimeFormat':fmt,'DateFormat':date,'Background':0x000055,'Foreground':0xFFFFFF,'Accent':0xFF55AA,11000:h,11001:m,11004:battery})
        for attempt in range(30):
            image=screenshot(options.monitor)
            try:result=check(image,h,m,fmt,date,palette,battery);break
            except AssertionError as failure:error=failure;time.sleep(.1)
        else:raise AssertionError(f'{name}: {error}')
        image.save(ROOT/f'media/ledger-{name}.png');evidence.append({'case':name,**result});print('PASS:',name,flush=True)
    (ROOT/'.tmp/native-checks.json').write_text(json.dumps(evidence,indent=2))
    labels=['Paper','Cream','Night','Sage','Ice','Blue']
    board=Image.new('RGB',(660,536),(32,32,32));draw=ImageDraw.Draw(board)
    for i,label in enumerate(labels):
        x=i%3*220+10;y=i//3*268;board.paste(Image.open(ROOT/f'media/ledger-palette-{i}.png'),(x,y));draw.text((x,y+236),label,fill='white')
    board.save(ROOT/'media/ledger-palettes.png')
    Image.open(ROOT/'media/ledger-default.png').resize((400,456),Image.Resampling.NEAREST).save(ROOT/'media/ledger-default-2x.png')
    send(keys,uuid,{'Palette':0,'TimeFormat':0,'DateFormat':1,11000:10,11001:8,11004:82})


if __name__=='__main__':main()
