/* LuckyRank.h
    原神抽卡概率计算工具包 GGanalysis 组件 LuckyRank
    用于计算抽卡运气排名
    注：计算过程忽视常驻中包含UP物品的情况
    by 一棵平衡树OneBST
*/

#include <stdio.h>
#include <stdlib.h>

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

#ifdef __cplusplus
extern "C"
{
#endif
/*计算带保底物品数量的运气排名*/
API_FUNC double APICALL rank_common_item(
    int get_num,        //已有物品抽取数量
    int use_pull,       //总共抽取次数
    int left_pull,      //距离获得上个物品又抽了多少
    double* pity_p,     //概率提升表
    int pity_pos        //保底抽数
);

#ifdef __cplusplus
} // __cplusplus defined.
#endif