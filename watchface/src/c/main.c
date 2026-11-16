#include <pebble.h>
#include "config.h"
#include "policy.h"
#include "fonts.h"
enum{P_PALETTE=1,P_BG,P_FG,P_ACCENT,P_TIME,P_DATE};
typedef struct{int palette,bg,fg,accent,time,date;}Settings;
static Settings s={0,0xFFFFFF,0,0xAA0000,0,1};
static const uint32_t PALETTES[6][3]={{0xFFFFFF,0,0xAA0000},{0xFFFFAA,0,0xAA0000},{0,0xFFFFFF,0xFF5500},{0xAAFFAA,0x005500,0x005500},{0xAAFFFF,0x000055,0x0055AA},{0x000055,0xFFFFFF,0x55FFFF}};
static Window *window;
static Layer *layer;
static struct tm current;
static int battery;
#if LEDGER_FIXTURE
static int fh=LEDGER_HOUR,fm=LEDGER_MINUTE,fb=LEDGER_BATTERY;
#endif
static const char *DAYS[]={"SUN","MON","TUE","WED","THU","FRI","SAT"};
static const char *MONTHS[]={"JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"};
static uint32_t color(int i){if(s.palette<6)return PALETTES[s.palette][i];return i==0?(uint32_t)s.bg:i==1?(uint32_t)s.fg:(uint32_t)s.accent;}
static void mask(GContext *ctx,const uint8_t *data,int width,int height,int stride,int x,int y){
 for(int row=0;row<height;row++){int start=-1;for(int col=0;col<=width;col++){
  bool on=col<width && (data[row*stride+col/8]&(0x80>>(col%8)));
  if(on && start<0)start=col;
  if(!on && start>=0){graphics_fill_rect(ctx,GRect(x+start,y+row,col-start,1),0,GCornerNone);start=-1;}
 }}
}
static void text(GContext *ctx,const char *value,int x,int y){
 for(int i=0;value[i];i++){unsigned char c=value[i];if(c>=32 && c<=90){int width=LABEL_WIDTH[c-32];mask(ctx,LABELS[c-32],width,20,4,x,y);x+=width+1;}else x+=6;}
}
#if defined(PBL_ROUND)
#include "round_digital.h"
static void round_numeral(GContext *ctx,int value,int x,int y,int w,int h){rmask(ctx,DIGITS[value],36,64,5,x,y,w,h);}
static void round_serif(GContext *ctx,const char *value,int x,int y,int w,int size,uint32_t ink){(void)size;int total=0;for(int i=0;value[i];i++){unsigned char c=value[i];total+=c>=32 && c<=90?LABEL_WIDTH[c-32]+1:6;}int h=10;if(total*h/20>w)h=w*20/total;int left=x+(w-total*h/20)/2;graphics_context_set_fill_color(ctx,GColorFromHEX(ink));for(int i=0;value[i];i++){unsigned char c=value[i];if(c>=32 && c<=90){int width=LABEL_WIDTH[c-32];rmask(ctx,LABELS[c-32],width,20,4,left,y,width*h/20>0?width*h/20:1,h);left+=(width+1)*h/20;}else left+=3;}}
static void round_current(GContext *ctx){uint32_t bg=color(0),fg=color(1),accent=color(2);RoundData d={0};d.now=current;d.bg=bg;d.fg=fg;d.accent=accent;d.battery=battery;d.time_mode=s.time;d.date_mode=s.date;int hour=rhour(&d);d.clock_shift=rpair_shift(DIGITS[hour/10],DIGITS[d.now.tm_min%10],36,64,5,18,132,30,49,90);d.label=round_serif;round_digital(ctx,&d,9,round_numeral);}
#endif
static void draw(Layer *own,GContext *ctx){
#if defined(PBL_ROUND)
 (void)own;round_current(ctx);rproof_marker(ctx);return;
#endif

 graphics_context_set_antialiased(ctx,false);
 graphics_context_set_fill_color(ctx,GColorFromHEX(color(0)));graphics_fill_rect(ctx,layer_get_bounds(own),0,GCornerNone);
 graphics_context_set_fill_color(ctx,GColorFromHEX(color(2)));graphics_fill_rect(ctx,GRect(13,20,174,3),0,GCornerNone);
 graphics_context_set_fill_color(ctx,GColorFromHEX(color(1)));
 if(!uses_24(s.time,clock_is_24h_style()))text(ctx,current.tm_hour>=12?"PM":"AM",text_left(current.tm_hour>=12?"PM":"AM"),28);
 int hour=display_hour(current.tm_hour,s.time,clock_is_24h_style());int values[4]={hour/10,hour%10,current.tm_min/10,current.tm_min%10};int offset=clock_offset(hour,current.tm_min);
 for(int i=0;i<4;i++)mask(ctx,DIGITS[values[i]],36,64,5,DIGIT_X[i]+offset,54);
 graphics_fill_circle(ctx,GPoint(99+offset,73),3);graphics_fill_circle(ctx,GPoint(99+offset,95),3);
 graphics_fill_rect(ctx,GRect(13,132,174,1),0,GCornerNone);
 char date[32]="";
 switch(s.date){
 case 1:snprintf(date,sizeof(date),"%s %s %02d",DAYS[current.tm_wday],MONTHS[current.tm_mon],current.tm_mday);break;
 case 2:snprintf(date,sizeof(date),"%04d-%02d-%02d",current.tm_year+1900,current.tm_mon+1,current.tm_mday);break;
 case 3:snprintf(date,sizeof(date),"%02d/%02d/%04d",current.tm_mon+1,current.tm_mday,current.tm_year+1900);break;
 case 4:snprintf(date,sizeof(date),"%02d/%02d/%04d",current.tm_mday,current.tm_mon+1,current.tm_year+1900);break;
 }
 text(ctx,date,text_left(date),145);graphics_fill_rect(ctx,GRect(13,181,174,1),0,GCornerNone);
 text(ctx,"BATTERY",13,194);char percent[8];snprintf(percent,sizeof(percent),"%d%%",battery);
 graphics_context_set_fill_color(ctx,GColorFromHEX(color(2)));text(ctx,percent,187-text_width(percent),194);
 graphics_context_set_fill_color(ctx,GColorFromHEX(color(1)));graphics_fill_rect(ctx,GRect(13,222,174,1),0,GCornerNone);
}
static void tick(struct tm *now,TimeUnits changed){(void)changed;current=*now;
#if LEDGER_FIXTURE
 current.tm_hour=fh;current.tm_min=fm;current.tm_year=126;current.tm_mon=10;current.tm_mday=5;current.tm_wday=4;
#endif
 layer_mark_dirty(layer);
}
static void battery_changed(BatteryChargeState state){battery=state.charge_percent;
#if LEDGER_FIXTURE
 battery=fb;
#endif
 layer_mark_dirty(layer);
}
static void set(DictionaryIterator *iter,uint32_t key,int persist,int maximum,int *target){Tuple *t=dict_find(iter,key);if(t && (t->type==TUPLE_INT || t->type==TUPLE_UINT)){int v=t->value->int32;if(v>=0 && v<=maximum){*target=v;persist_write_int(persist,v);}}}
#if LEDGER_FIXTURE
static void fixture(DictionaryIterator *iter,int key,int maximum,int *target){Tuple *t=dict_find(iter,key);if(t && t->type==TUPLE_INT && t->value->int32>=0 && t->value->int32<=maximum)*target=t->value->int32;}
#endif
static void inbox(DictionaryIterator *iter,void *context){
#if defined(PBL_ROUND) && (LEDGER_FIXTURE)
 Tuple *round_proof=dict_find(iter,11022);if(round_proof && round_proof->type==TUPLE_INT){r_proof=round_proof->value->int32==1;layer_mark_dirty(layer);}
#endif
(void)context;
 set(iter,MESSAGE_KEY_Palette,P_PALETTE,6,&s.palette);set(iter,MESSAGE_KEY_Background,P_BG,0xFFFFFF,&s.bg);set(iter,MESSAGE_KEY_Foreground,P_FG,0xFFFFFF,&s.fg);set(iter,MESSAGE_KEY_Accent,P_ACCENT,0xFFFFFF,&s.accent);set(iter,MESSAGE_KEY_TimeFormat,P_TIME,2,&s.time);set(iter,MESSAGE_KEY_DateFormat,P_DATE,4,&s.date);
#if LEDGER_FIXTURE
 fixture(iter,11000,23,&fh);fixture(iter,11001,59,&fm);fixture(iter,11004,100,&fb);battery=fb;
#endif
 time_t now=time(NULL);tick(localtime(&now),MINUTE_UNIT);
}
static void restore(int key,int maximum,int *target){if(persist_exists(key)){int v=persist_read_int(key);if(v>=0 && v<=maximum)*target=v;}}
static void init(void){
 restore(P_PALETTE,6,&s.palette);restore(P_BG,0xFFFFFF,&s.bg);restore(P_FG,0xFFFFFF,&s.fg);restore(P_ACCENT,0xFFFFFF,&s.accent);restore(P_TIME,2,&s.time);restore(P_DATE,4,&s.date);
 window=window_create();layer=layer_create(PBL_IF_ROUND_ELSE(GRect(0,0,PBL_DISPLAY_WIDTH,PBL_DISPLAY_HEIGHT),GRect(0,0,200,228)));layer_set_update_proc(layer,draw);layer_add_child(window_get_root_layer(window),layer);window_stack_push(window,true);time_t now=time(NULL);tick(localtime(&now),MINUTE_UNIT);battery_changed(battery_state_service_peek());tick_timer_service_subscribe(MINUTE_UNIT,tick);battery_state_service_subscribe(battery_changed);app_message_register_inbox_received(inbox);app_message_open(256,64);
}
static void deinit(void){tick_timer_service_unsubscribe();battery_state_service_unsubscribe();app_message_deregister_callbacks();layer_destroy(layer);window_destroy(window);}
int main(void){init();app_event_loop();deinit();}
