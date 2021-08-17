/* GGanalysis.h
    原神抽卡概率计算工具包 GGanalysis
    by 一棵平衡树OneBST
*/
#include <stdio.h>
#include <stdlib.h>
/*
#ifdef OPENMP_PARALLEL
#include <omp.h>
#endif
*/
// https://www.transmissionzero.co.uk/computing/building-dlls-with-mingw/
/* You should define ADD_EXPORTS *only* when building the DLL. */
#ifdef _WIN32

    /* You should define ADD_EXPORTS *only* when building the DLL. */
    #ifdef API_EXPORTS
        #define API_FUNC __declspec(dllexport)
    #else
        #define API_FUNC __declspec(dllimport)
    #endif

  /* Define calling convention in one place, for convenience. */
  #define APICALL __cdecl

#else /* _WIN32 not defined. */

    /* Define with no value on non-Windows OSes. */
    #define API_FUNC
    #define APICALL

#endif

/* Make sure functions are exported with C linkage under C++ compilers. */

#ifdef __cplusplus
extern "C"
{
#endif

/* Declare our Add function using the above definitions. */
/*带保底物品DP*/
API_FUNC void APICALL pity_item_DP(
    double* ans,        //DP结果存放数组
    int item_num,       //计算物品抽取数量
    int calc_pull,      //计算抽数
    double* pity_p,     //概率提升表
    int pity_pos,       //保底抽数
    int pull_state      //垫抽情况
);
/*UP类型物品DP*/
API_FUNC void APICALL GI_upitem_DP(
    double* ans,        //DP结果存放数组
    int item_num,       //计算物品抽取数量
    int calc_pull,      //计算抽取次数
    double* pity_p,     //概率提升表
    int pity_pos,       //保底抽数
    double up_rate,     //UP概率  
    int up_type,        //UP物品种类
    int pull_state,     //垫抽情况
    int up_guarantee,   //大保底
    int want_in_stander,//想要的是否在常驻
    int up_in_stander,  //UP物品在常驻池中的数量
    int stander_num     //常驻池中物品数量
);
/*武器池神铸定轨DP*/
API_FUNC void APICALL GI_weapon_EP_DP(
    double* ans,        //DP结果存放数组
    int item_num,       //计算物品抽取数量
    int calc_pull,      //计算抽取次数
    double* pity_p,     //概率提升表
    int pity_pos,       //保底抽数
    double up_rate,     //UP概率  
    int up_type,        //UP物品种类
    int pull_state,     //垫抽情况
    int up_guarantee,   //大保底情况
    int want_in_stander,//想要的是否在常驻
    int up_in_stander,  //UP物品在常驻池中的数量
    int stander_num     //常驻池中物品数量
);
/*常驻池DP*/
API_FUNC void APICALL GI_stander_DP(
    double* ans,        //DP结果存放数组
    int item_num,       //计算物品抽取数量
    int calc_pull,      //计算抽数
    double* pity_p,     //概率提升表
    int pity_pos,       //保底抽数
    double* hit_p,      //类别概率表
    int hit_pos,        //类别保底
    int pull_state,     //垫抽情况
    int type_state,     //多少抽没有异类物品
    int last_type,      //上次五星种类
    int stander_num,    //常驻池中本类物品数量
    int collect_all     //是否计算收集齐全概率
);
#ifdef __cplusplus
} // __cplusplus defined.
#endif