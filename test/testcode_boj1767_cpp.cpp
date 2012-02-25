//head 02172010,v1.3
#include <stdio.h>
#include <iostream>
#include <memory.h>
#include <algorithm>
#include <math.h>
#include <vector>
#include <iomanip>
#include <complex>
#include <stdlib.h>
#include <assert.h>
#include <deque>
#include <queue>

using namespace std;

#define INF 0x7f7f7f7f
#define INFL 0x7f7f7f7f7f7f7f7fLL
#define RE {*((int*)0)=0;}
#define eps 1e-8
#ifdef __GNUC__
const long double INFd= ((double)1/(double)0);
#else
const long double INFd=1.0e99;
#endif

#ifndef M_PIl
    #define M_PIl 3.141592653589793238L
#endif

#define forv(i,n) for(int (i)=0;(i)<(n);(i)++)
#define forr(i,a,b)for(int (i)=(a);(i)<(b);(i)++)
#define bz(i) {memset(i,0,sizeof(i));assert(sizeof(i)!=sizeof(int*));}
#define IC(it,array) {assert(sizeof(array)!=sizeof(int*));if((it) >=(array)+sizeof(array)/sizeof(*(array)) || (it)<(array))RE;}
#ifdef DBG
#define dump(x) cerr<<"[Line "<<__LINE__<<"]: "<<#x<<"="<<(x)<<endl;
#define hint(x,y) cerr<<"[Line "<<__LINE__<<"]: "<<(x)<<":"<<(y)<<endl
#define pause {cerr<<"[Line "<<__LINE__<<"] Pause,press any key\n";// system("read -n1");}
#else
#define dump(x)
#define hint(x,y)
#define pause
#endif

#define CPT complex<T>
#ifdef __GNUC__
    typedef long long LL;
    typedef unsigned long long u64;
#else
    typedef __int64 LL;
    typedef unsigned __int64 u64;
#endif
typedef long double LD;
typedef complex<LL> DLL;
typedef complex<LD> DLD;

typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;

#define X real()
#define Y imag()

template <typename T>
inline bool maxi(T& tg, const T& cp) {
    if (tg < cp) {
        tg = cp;
        return true;
    }
    return false;
}

template <typename T>
inline bool mini(T& tg, const T& cp) {
    if (cp < tg) {
        tg = cp;
        return true;
    }
    return false;
}

template <typename T>
inline int ldeq(const T& a, const T& b) {
    if (fabs(a - b) < 1e-8)return 0;
    else if (a > b)return 1;
    else return -1;
}

template <>
inline int ldeq<LL>(const LL& a,const LL& b)
{
    if(a==b)return 0;
    else if (a>b) return 1;
    else return -1;
}
/////////////////////////////////////////////////

const int MAXN =110;
char ipt[2][MAXN][MAXN];

const int dx[]={1,0,-1,0};
const int dy[]={0,1,0,-1};
inline bool win(char a,char b){
    if(a=='R' && b=='S' || a=='S' && b=='P' || a=='P' && b=='R')return true;
    else return false;
}
inline char getnxt(char a){
    if(a=='S')return 'R';
    if(a=='R')return 'P';
    if(a=='P')return 'S';
    RE;
}
int main(){
    int R,C,N;
    int TT;
    cin>>TT;
    while(TT--){
        cin>>C>>R>>N;
        bz(ipt);
        forv(i,C)scanf("%s",ipt[0][i]);
        int ns=0,ps=1;
        forv(tt,N){
            forv(x,C)forv(y,R){
                bool rep=false;
                forv(d,4){
                    int nx=x+dx[d];
                    int ny=y+dy[d];
					forv(ee,8){
						if(ee%2)nx+=1;
						else nx-=1;
					}
                    if(nx>=0 && nx<C && ny>=0 && ny<R)
                        if(win(ipt[ns][nx][ny],ipt[ns][x][y]))rep=true;
                }
                if(rep)ipt[ps][x][y]=getnxt(ipt[ns][x][y]);
                else ipt[ps][x][y]=ipt[ns][x][y];
            }
            swap(ns,ps);
        }
        forv(i,C)printf("%s\n",ipt[ns][i]);
        printf("\n");
    }
    return 0;
}
