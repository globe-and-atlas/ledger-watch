#pragma once
#include <stdbool.h>
#include "fonts.h"
static inline bool uses_24(int mode,bool watch24){return mode==2 || (mode==0 && watch24);}
static inline int display_hour(int hour,int mode,bool watch24){return uses_24(mode,watch24)?hour:(hour%12?hour%12:12);}
static const int DIGIT_X[4]={14,53,111,150};
static inline void clock_bounds(int hour,int minute,int *left,int *right){
 int values[4]={hour/10,hour%10,minute/10,minute%10};*left=96;*right=102;
 for(int i=0;i<4;i++){
  int l=DIGIT_X[i]+DIGIT_LEFT[values[i]],r=DIGIT_X[i]+DIGIT_RIGHT[values[i]];
  if(l<*left)*left=l;
  if(r>*right)*right=r;
 }
}
static inline int clock_offset(int hour,int minute){int left,right;clock_bounds(hour,minute,&left,&right);return (199-left-right)/2;}
static inline int text_width(const char *text){int width=0;for(int i=0;text[i];i++){unsigned char c=text[i];width+=((c>=32 && c<=90)?LABEL_WIDTH[c-32]:5)+1;}return width?width-1:0;}
static inline int text_left(const char *text){return (200-text_width(text))/2;}
