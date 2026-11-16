"""Generate readable one-bit Book serif numerals and proportional labels."""
from pathlib import Path
from functools import lru_cache
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
FONT=ROOT/'assets/fonts/GridcoreBook-700.ttf'
LABEL_FONT=ROOT/'assets/fonts/LibreBaskerville-Variable.ttf'


@lru_cache(maxsize=None)
def digit_mask(n):
    font=ImageFont.truetype(str(FONT),200);boxes=[font.getbbox(str(d)) for d in range(10)]
    top=min(b[1] for b in boxes);bottom=max(b[3] for b in boxes);maximum=max(b[2]-b[0] for b in boxes);box=boxes[n]
    canvas=Image.new('L',(box[2]-box[0],bottom-top));ImageDraw.Draw(canvas).text((-box[0],-top),str(n),font=font,fill=255)
    canvas=canvas.resize((round(canvas.width*34/maximum),64),Image.Resampling.LANCZOS)
    image=Image.new('L',(40,64));image.paste(canvas,((36-canvas.width)//2,0))
    return image.point(lambda p:255 if p>=112 else 0).convert('1')


@lru_cache(maxsize=None)
def label_mask(char):
    font=ImageFont.truetype(str(LABEL_FONT),48)
    try:font.set_variation_by_axes([700])
    except OSError:pass  # Static fonts have no axes; glyph coverage is still required.
    allowed='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ%/-'
    missing=font.getmask('\ufffd')
    for c in allowed:
        actual=font.getmask(c)
        assert actual.size!=missing.size or bytes(actual)!=bytes(missing),f'Missing label glyph: {c}'
    boxes=[font.getbbox(c) for c in allowed];top=min(b[1] for b in boxes);bottom=max(b[3] for b in boxes)
    if char not in allowed:return Image.new('1',(32,20)),5
    b=font.getbbox(char);canvas=Image.new('L',(b[2]-b[0],bottom-top));ImageDraw.Draw(canvas).text((-b[0],-top),char,font=font,fill=255)
    width=max(1,round(canvas.width*20/(bottom-top)));canvas=canvas.resize((width,20),Image.Resampling.LANCZOS)
    canvas=canvas.point(lambda p:255 if p>=112 else 0).convert('1');bounds=canvas.getbbox()
    if bounds:canvas=canvas.crop((bounds[0],0,bounds[2],20))
    width=canvas.width;assert width<=32
    image=Image.new('1',(32,20));image.paste(canvas,(0,0));return image,width


def main():
    masks=[digit_mask(i) for i in range(10)];labels=[label_mask(chr(c)) for c in range(32,91)]
    rows=['/* Generated Book serif masks; OFL license in licenses/. */','#pragma once','#include <stdint.h>',
          'static const uint8_t DIGITS[10][320]={']
    rows.extend('{'+','.join(map(str,m.tobytes()))+'},' for m in masks);rows.append('};')
    rows.append('static const int DIGIT_LEFT[10]={'+','.join(str(m.getbbox()[0]) for m in masks)+'};')
    rows.append('static const int DIGIT_RIGHT[10]={'+','.join(str(m.getbbox()[2]-1) for m in masks)+'};')
    rows.append('static const uint8_t LABELS[59][80]={')
    rows.extend('{'+','.join(map(str,m.tobytes()))+'},' for m,w in labels);rows.append('};')
    rows.append('static const uint8_t LABEL_WIDTH[59]={'+','.join(str(w) for m,w in labels)+'};')
    (ROOT/'watchface/src/c/fonts.h').write_text('\n'.join(rows)+'\n')
    for text in ['THU NOV 05','WED SEP 30','2026-11-05','BATTERY','100%']:
        width=sum(labels[ord(c)-32][1]+1 for c in text)-1;print(text,width)


if __name__=='__main__':main()
