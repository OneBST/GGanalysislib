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
    int i,j,pull;
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
    double state = 1.0;
    for(i=1; i<=pity_pos; i++)
    {
        p_trans[i] = state * pity_p[i];
        state = state * (1.0 - pity_p[i]);
        p_fail[i]  = state;
    }
    p_fail[0] = 1.0;      //垫了0抽辅助概率

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

/*计算带UP物品数量的运气排名 忽略常驻池*/
double APICALL rank_up_item(
    int get_num,        //已有物品抽取数量
    int use_pull,       //总共抽取次数
    int left_pull,      //距离获得上个物品又抽了多少
    int up_guarantee,   //大保底情况
    double* pity_p,     //概率提升表
    int pity_pos,       //保底抽数
    double up_rate,     //UP概率  
    int up_type         //UP物品种类
)
{
    int i,j,pull;
    //DP数组声明
    double*** M;
    double* temp_storage = malloc((get_num+1) * (use_pull+1) * 3 * sizeof(double));
    for(i=0; i<(get_num+1)*(use_pull+1)*3; i++)
        temp_storage[i] = 0;
    //M中最后一个维度 0表示抽到想要UP 1表示抽到不想要UP 2表示没抽到UP
    M = build_3D_index(temp_storage, get_num+1, use_pull+1, 3);
    
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
    M[0][0][0] = 1;

    double up_trans;        //多UP选中想要物品的概率
    int last_pos;           //开始转移概率位置
    up_trans = 1.0/(double)up_type;
    
    //DP部分
    for(i=0; i<=get_num; i++)//从零开始，用于记录先歪再抽的情况
    {
        for(j=1; j<=use_pull; j++)
        {
            for(pull=1; pull<=(pity_pos>j?j:pity_pos); pull++)
            {
                last_pos = j-pull;
                //想要的UP
                if(i)
                {
                    M[i][j][0] += up_rate * M[i-1][last_pos][0] * up_trans * p_trans[pull];
                    M[i][j][0] += up_rate * M[i-1][last_pos][1] * up_trans * p_trans[pull];
                    M[i][j][0] += M[i-1][last_pos][2] * up_trans * p_trans[pull];
                }
                //其他UP
                if(up_type>1)
                {
                    M[i][j][1] += up_rate * M[i][last_pos][0] * (1.0-up_trans) * p_trans[pull];
                    M[i][j][1] += up_rate * M[i][last_pos][1] * (1.0-up_trans) * p_trans[pull];
                    M[i][j][1] += M[i][last_pos][2] * (1.0-up_trans) * p_trans[pull];
                }            
                //非UP
                M[i][j][2] += (1-up_rate) * M[i][last_pos][0] * p_trans[pull];
                M[i][j][2] += (1-up_rate) * M[i][last_pos][1] * p_trans[pull];
            }
        }
    }

    //抽了i抽都没有物品时，抽到物品的条件期望抽数
    double* conditional_expectation = malloc(pity_pos * sizeof(double));
    conditional_expectation[pity_pos-1] = 1.0;  //再抽一次必出，期望为1
    for(i=pity_pos-2; i>=0; i--)
        conditional_expectation[i] = (conditional_expectation[i+1]+1) * (1-pity_p[i+1])
                                    + pity_p[i+1];
    // for(i=0; i<pity_pos; i++)
    //     printf("%d %lf\n", i, conditional_expectation[i]);
    // if(up_guarantee == 0)
    //     printf("up_guarantee=0!\n");
    double ans = 0.0;
    double refer_e;     //从零抽特定UP物品的期望
    double test_e;      //输入情况期望
    double case_e;      //列举条件的期望
    refer_e = (2.0-up_rate) * up_type *conditional_expectation[0];
    // printf("up_rate=%lf up_type=%d refer_e=%lf\n", up_rate, up_type, refer_e);
    if(up_guarantee == 0)//没有大保底情况下抽一个特定UP物品期望
    {
        test_e =
            //抽到UP并抽到想要的UP 
            up_rate / up_type * conditional_expectation[left_pull] +   
            //抽到UP但没有抽到想要的UP
            up_rate * ((up_type-1.0) / up_type) * (conditional_expectation[left_pull]+refer_e) +
            //没抽到UP下一抽抽到UP
            (1.0-up_rate) * (1.0 / up_type) * (conditional_expectation[left_pull]+conditional_expectation[0]) +
            //没抽到UP下一抽也没抽到UP
            (1.0-up_rate) * ((up_type-1.0) / up_type) * (conditional_expectation[left_pull]+conditional_expectation[0]+refer_e);
        // printf("left_pull=%d C_e=%lf\n", left_pull, conditional_expectation[left_pull]);
    }
    else//有大保底情况下抽一个特定UP物品期望
        test_e =
            //抽到UP并抽到想要的UP
            1.0 / up_type * conditional_expectation[left_pull] +
            //抽到UP但没有抽到想要的UP
            ((up_type-1.0) / up_type) * (conditional_expectation[left_pull]+refer_e);
    // printf("test_e = %lf\n", test_e);

    //将更差的情况加起来 对于有无大保底的情况按照再抽一个UP物品的期望抽数排序
    for(i=0; i<=get_num; i++)   //抽了多少个
    {
        for(j=0; j<pity_pos; j++)
        {
            if(use_pull - j < 0)
                break;
            if(i==get_num)//抽到物品数量相同时，比较再抽一个物品的期望
                case_e = 
                    //抽到UP并抽到想要的UP 
                    up_rate / up_type * conditional_expectation[j] +   
                    //抽到UP但没有抽到想要的UP
                    up_rate * ((up_type-1) / up_type) * (conditional_expectation[j]+refer_e) +
                    //没抽到UP下一抽抽到UP
                    (1-up_rate) * (1 / up_type) * (conditional_expectation[j]+conditional_expectation[0]) +
                    //没抽到UP下一抽也没抽到UP
                    (1-up_rate) * ((up_type-1) / up_type) * (conditional_expectation[j]+conditional_expectation[0]+refer_e);
            if(!((case_e <= test_e) && (i == get_num)))//如果不是更好或者相同的情况
            {
                ans += M[i][use_pull-j][0] * p_fail[j];
                ans += M[i][use_pull-j][1] * p_fail[j];
            }
            //枚举带有大保底的情况
            if(i==get_num)
                case_e =
                    //抽到UP并抽到想要的UP
                    1 / up_type *conditional_expectation[j] +
                    //抽到UP但没有抽到想要的UP
                    ((up_type-1) / up_type) * (conditional_expectation[j]+refer_e);
            // if(i==get_num)printf("GG: %d %lf\n", j, case_e);
            if(!((case_e <= test_e) && (i == get_num)))//如果不是更好或者相同的情况
                ans += M[i][use_pull-j][2] * p_fail[j];
        }
    }
    return ans;
}