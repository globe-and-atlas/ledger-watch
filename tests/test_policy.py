from pathlib import Path
import importlib.util
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def test_native_geometry():
    source = ROOT / '.tmp/policy.c'
    binary = ROOT / '.tmp/policy'
    source.write_text('''#include <assert.h>
#include <stdio.h>
#include "policy.h"
int main(void){
 for(int h=0;h<24;h++){
  assert(display_hour(h,2,false)==h);
  assert(display_hour(h,1,true)==(h%12?h%12:12));
  assert(display_hour(h,0,true)==h);
  assert(display_hour(h,0,false)==(h%12?h%12:12));
  for(int m=0;m<60;m++){
   int l,r;clock_bounds(h,m,&l,&r);int offset=clock_offset(h,m);
   assert(l+offset>=10);assert(r+offset<190);
   assert(l+r+2*offset>=198 && l+r+2*offset<=200);
  }
 }
 const char *days[]={"SUN","MON","TUE","WED","THU","FRI","SAT"};
 const char *months[]={"JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"};
 for(int d=0;d<7;d++)for(int m=0;m<12;m++)for(int n=1;n<=31;n++){
  char date[32];snprintf(date,sizeof(date),"%s %s %02d",days[d],months[m],n);assert(text_width(date)<=174);
 }
 assert(text_width("2026-11-05")<=174);assert(text_width("11/05/2026")<=174);assert(text_width("05/11/2026")<=174);
 assert(13+text_width("BATTERY")+10<187-text_width("100%"));
 return 0;}
''')
    subprocess.run(['cc', '-Wall', '-Wextra', '-Werror', '-I', str(ROOT/'watchface/src/c'), str(source), '-o', str(binary)], check=True)
    subprocess.run([str(binary)], check=True)


def test_serif_masks_retain_strokes():
    spec = importlib.util.spec_from_file_location('fonts', ROOT/'execution/generate_fonts.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for n in range(10):
        image = module.digit_mask(n)
        assert image.getbbox()[2] <= 36
        assert all(image.crop((0,y,36,y+1)).getbbox() for y in range(image.getbbox()[1],image.getbbox()[3]))
    assert module.label_mask('W')[1] <= 32


def test_label_glyph_coverage_rejects_numeral_subset(monkeypatch):
    import pytest
    spec=importlib.util.spec_from_file_location('coverage_fonts',ROOT/'execution/generate_fonts.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ%/-':assert module.label_mask(c)[0].getbbox()
    module.label_mask.cache_clear()
    monkeypatch.setattr(module,'LABEL_FONT',module.FONT)
    with pytest.raises(AssertionError,match='Missing label glyph'):
        module.label_mask('A')
