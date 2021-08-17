#include "LuckyRank.h"
#include "MyTools.h"


/*计算带保底物品数量的运气排名*/
double APICALL rank_common_item(
    int get_num,        //已有物品抽取数量
    int use_pull,       //总共抽取次数
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
    M = build_2D_index(temp_storage, get_num+1, use_pull+1);
    
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

#ifdef XXXX
/*计算带UP物品数量的运气排名*/
void APICALL rank_up_item(
    int get_num,        //已有物品抽取数量
    int use_pull,       //总共抽取次数
    int left_pull,      //距离获得上个物品又抽了多少
    double* pity_p,     //概率提升表
    int pity_pos,       //保底抽数
    double up_rate,     //UP概率  
    int up_type         //UP物品种类
)
{
    int i,j,k,pull;
    //DP数组声明
    double*** M;
    double* temp_storage = malloc((item_num+1) * (calc_pull+1) * 3 * sizeof(double));
    for(i=0; i<(item_num+1)*(calc_pull+1)*3; i++)
        temp_storage[i] = 0;
    //M中最后一个维度 0表示抽到想要UP 1表示抽到不想要UP 2表示没抽到UP
    M = build_3D_index(temp_storage, item_num+1, calc_pull+1, 3);
    
    //用于状态转移的概率 从恰好抽到一个物品转移到恰好抽到另一个物品
    double* p_normal = calc_distribution(pity_p, pity_pos);
    //处理垫抽的预处理
    //用于处理初始有垫抽数情况的修正常数
    double fix_const = 0;
    for(i=pull_state+1; i<=pity_pos; i++)
        fix_const = fix_const + p_normal[i];
    //修正转移概率
    double* p_first = malloc((pity_pos+1) * sizeof(double));
    for(i=pull_state+1; i<=pity_pos; i++)
        p_first[i-pull_state] = p_normal[i]/fix_const;
    for(i=pity_pos-pull_state+1; i<=pity_pos; i++)
        p_first[i] = 0;

    //设置DP初始条件
    //若有大保底
    if(up_guarantee)
        M[0][0][2] = 1;
    //没有大保底
    else
        M[0][0][0] = 1;
    double* p_trans;        //恰好在本抽抽到概率
    double up_trans;        //多UP选中想要角色的概率
    double stander_trans;   //常驻池中选取到想要UP概率
    double stander_other;   //常驻池中选取到其他UP概率
    double stander_notup;   //常驻池中选取到非UP概率
    int last_pos;           //开始转移概率位置
    up_trans = 1.0/(double)up_type;
    //处理从常驻中歪的情况
    stander_trans = (double)want_in_stander/(double)stander_num;
    stander_other = (double)(up_in_stander - want_in_stander)/(double)stander_num;
    stander_notup = (double)(stander_num - up_in_stander)/(double)stander_num;
    
    //DP部分
    for(i=0; i<=item_num; i++)//从零开始，用于记录先歪再抽的情况
    {
        for(j=1; j<=calc_pull; j++)
        {
            for(pull=1; pull<=(pity_pos>j?j:pity_pos); pull++)
            {
                last_pos = j-pull;
                if(last_pos)    //非从零开始
                    p_trans = p_normal;
                else            //从零开始
                    p_trans = p_first;
                //想要的UP
                if(i)
                {
                    M[i][j][0] += up_rate * M[i-1][last_pos][0] * up_trans * p_trans[pull];
                    M[i][j][0] += up_rate * M[i-1][last_pos][1] * up_trans * p_trans[pull];
                    M[i][j][0] += stander_trans * (1-up_rate) * M[i-1][last_pos][0] * p_trans[pull];
                    M[i][j][0] += stander_trans * (1-up_rate) * M[i-1][last_pos][1] * p_trans[pull];
                    M[i][j][0] += M[i-1][last_pos][2] * up_trans * p_trans[pull];
                }
                //其他UP
                if(up_type>1)
                {
                    M[i][j][1] += up_rate * M[i][last_pos][0] * (1-up_trans) * p_trans[pull];
                    M[i][j][1] += up_rate * M[i][last_pos][1] * (1-up_trans) * p_trans[pull];
                    M[i][j][1] += stander_other * (1-up_rate) * M[i][last_pos][0] * p_trans[pull];
                    M[i][j][1] += stander_other * (1-up_rate) * M[i][last_pos][1] * p_trans[pull];
                    M[i][j][1] += M[i][last_pos][2] * (1-up_trans) * p_trans[pull];
                }            
                //非UP
                M[i][j][2] += stander_notup * (1-up_rate) * M[i][last_pos][0] * p_trans[pull];
                M[i][j][2] += stander_notup * (1-up_rate) * M[i][last_pos][1] * p_trans[pull];
            }
        }
    }

    /*结果提取部分*/
    int temp_pos;
    for(i=0; i<(item_num+1)*(calc_pull+1); i++)
        ans[i] = 0;
    //梯形累加
    /* for(i=1; i<=item_num; i++)
        for(j=1; j<=calc_pull; j++)
        {
            temp_pos = i * (calc_pull+1) + j;
            ans[temp_pos] = ans[temp_pos-1] + M[i][j][0];
        }
    */
    //不累加，返回恰好在某抽抽到的概率
    for(i=1; i<=item_num; i++)
        for(j=1; j<=calc_pull; j++)
        {
            temp_pos = i * (calc_pull+1) + j;
            ans[temp_pos] = M[i][j][0];
        }
    return;
}
#endif