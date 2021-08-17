#include "LuckyRank.h"

/*给一维数组加上二维索引*/
double** build_2D_index_local(double* storage, int rows, int cols)
{
    int i;
    double **index_ptr, *temp_ptr;
    index_ptr = (double**)malloc(rows * sizeof(void*));
    temp_ptr = storage;
    for(i=0; i<rows; i++)
    {
        index_ptr[i] = temp_ptr;
        temp_ptr += cols;
    }
    return index_ptr;
}


/*计算带保底物品数量的运气排名*/
double APICALL rank_common_item(
    int get_num,        //已有物品抽取数量
    int use_pull,      //总共抽取次数
    int left_pull,      //距离获得上个物品又抽了多少
    double* pity_p,     //概率提升表
    int pity_pos        //保底抽数
)
{
    int i,j,k,pull;
    /*DP数组声明*/
    double** M;
    double* temp_storage = malloc((get_num+1) * (use_pull+1) * sizeof(double));
    for(i=0; i<(get_num+1)*(use_pull+1); i++)
        temp_storage[i] = 0;
    M = build_2D_index_local(temp_storage, get_num+1, use_pull+1);
    
    /*预处理用于状态转移的概率*/ 
    double* p_trans;    //从恰好抽到一个物品转移到恰好抽到另一个物品
    double* p_fail;     //从恰好抽到一个物品转移到再用i抽没有抽到物品
    p_trans = malloc((pity_pos+1) * sizeof(double));
    p_fail  = malloc((pity_pos+1) * sizeof(double));
    double state = 1;
    for(i=1; i<=pity_pos; i++)
    {
        p_trans[i] = state * pity_p[i];
        state = state * (1.0 - pity_p[i]);
        p_fail[i]  = state;
    }
    p_fail[0] = 1;      //垫了0抽辅助概率
    //设置DP初始条件
    M[0][0] = 1;
    int last_pos;       //开始转移概率位置
    
    //DP部分
    for(i=1; i<=get_num; i++)
        for(j=1; j<=use_pull; j++)
            for(pull=1; pull<=(pity_pos>j?j:pity_pos); pull++)
            {
                last_pos = j-pull;
                //j抽抽到i个想要的物品
                M[i][j] += M[i-1][last_pos] * p_trans[pull];
            }
    double ans = 0;
    int calc_end_pos;
    for(i=0; i<=get_num; i++)   //抽了多少个
    {
        calc_end_pos = pity_pos;
        if(i == get_num)
            calc_end_pos = left_pull;
        for(j=0; j<calc_end_pos; j++)
        {
            if(use_pull - j < 0)
                break;
            ans += M[i][use_pull-j] * p_fail[j];
        }
    }
    return ans;
}

