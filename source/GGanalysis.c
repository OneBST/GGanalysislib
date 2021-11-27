/* GGanalysis.c
    原神抽卡概率计算工具包 GGanalysis
    by 一棵平衡树OneBST
*/

#include "GGanalysis.h"
#include "MyTools.h"

/*计算抽到物品的分布情况*/
double* calc_distribution(double* pity_p, int pity_pos)
{
    double* ans = malloc((pity_pos+1) * sizeof(double));
    double state = 1;
    int i;
    for(i=1; i<=pity_pos; i++)
    {
        ans[i] = state * pity_p[i];
        state = state * (1.0 - pity_p[i]);
    }
    return ans;
}

/*带保底物品DP*/
void APICALL pity_item_DP(
    double* ans,        //DP结果存放数组
    int item_num,       //计算物品抽取数量
    int calc_pull,      //计算抽数
    double* pity_p,     //概率提升表
    int pity_pos,       //保底抽数
    int pull_state      //垫抽情况
)
{
    int i,j,pull;
    //DP数组声明
    double** M;
    double* temp_storage = malloc((item_num+1) * (calc_pull+1) * sizeof(double));
    for(i=0; i<(item_num+1)*(calc_pull+1); i++)
        temp_storage[i] = 0;
    M = build_2D_index(temp_storage, item_num+1, calc_pull+1);
    
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
    M[0][0] = 1;

    double* p_trans;        //恰好在本抽抽到概率
    int last_pos;           //开始转移概率位置
    
    //DP部分
    for(i=1; i<=item_num; i++)
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
                //想要的物品
                M[i][j] += M[i-1][last_pos] * p_trans[pull];
            }
        }
    }

    /*结果提取部分*/
    int temp_pos;
    for(i=0; i<(item_num+1)*(calc_pull+1); i++)
        ans[i] = 0;
    //不累加，返回恰好在某抽抽到的概率
    for(i=1; i<=item_num; i++)
        for(j=1; j<=calc_pull; j++)
        {
            temp_pos = i * (calc_pull+1) + j;
            ans[temp_pos] = M[i][j];
        }
    return;
}


/*UP类型物品DP*/
void APICALL GI_upitem_DP(
    double* ans,        //DP结果存放数组
    int item_num,       //计算物品抽取数量
    int calc_pull,      //计算抽数
    double* pity_p,     //概率提升表
    int pity_pos,       //保底抽数
    double up_rate,     //UP概率  
    int up_type,        //UP物品种类
    int pull_state,     //垫抽情况
    int up_guarantee,   //大保底情况
    int want_in_stander,//想要的是否在常驻
    int up_in_stander,  //UP物品在常驻池中的数量
    int stander_num     //常驻池中物品数量
)
{
    int i,j,pull;
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
                    M[i][j][0] += stander_trans * (1.0-up_rate) * M[i-1][last_pos][0] * p_trans[pull];
                    M[i][j][0] += stander_trans * (1.0-up_rate) * M[i-1][last_pos][1] * p_trans[pull];
                    M[i][j][0] += M[i-1][last_pos][2] * up_trans * p_trans[pull];
                }
                //其他UP
                if(up_type>1)
                {
                    M[i][j][1] += up_rate * M[i][last_pos][0] * (1.0-up_trans) * p_trans[pull];
                    M[i][j][1] += up_rate * M[i][last_pos][1] * (1.0-up_trans) * p_trans[pull];
                    M[i][j][1] += stander_other * (1.0-up_rate) * M[i][last_pos][0] * p_trans[pull];
                    M[i][j][1] += stander_other * (1.0-up_rate) * M[i][last_pos][1] * p_trans[pull];
                    M[i][j][1] += M[i][last_pos][2] * (1.0-up_trans) * p_trans[pull];
                }            
                //非UP
                M[i][j][2] += stander_notup * (1.0-up_rate) * M[i][last_pos][0] * p_trans[pull];
                M[i][j][2] += stander_notup * (1.0-up_rate) * M[i][last_pos][1] * p_trans[pull];
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


/*武器池神铸定轨DP*/
void APICALL GI_weapon_EP_DP(
    double* ans,        //DP结果存放数组
    int item_num,       //计算物品抽取数量
    int calc_pull,      //计算抽数
    double* pity_p,     //概率提升表
    int pity_pos,       //保底抽数
    double up_rate,     //UP概率  
    int up_type,        //UP物品种类
    int pull_state,     //垫抽情况
    int up_guarantee,   //大保底情况
    int want_in_stander,//想要的是否在常驻
    int up_in_stander,  //UP物品在常驻池中的数量
    int stander_num     //常驻池中物品数量
)
{
    int i,j,pull;
    //DP数组声明
    double*** M;
    double* temp_storage = malloc((item_num+1) * (calc_pull+1) * 4 * sizeof(double));
    for(i=0; i<(item_num+1)*(calc_pull+1)*4; i++)
        temp_storage[i] = 0;
    
    M = build_3D_index(temp_storage, item_num+1, calc_pull+1, 4);
    
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
    //up_guarantee 中数字表示初始状态
    M[0][0][up_guarantee] = 1;
    
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
                /*
                M中维度说明
                0 表示抽到想要的UP  命定值为0
                1 表示抽到不想要UP  命定值为1
                2 表示抽到了常驻    命定值为1
                3 表示             命定值为2
                */
                //想要的UP
                if(i)
                {
                    M[i][j][0] += up_rate * M[i-1][last_pos][0] * up_trans * p_trans[pull];
                    M[i][j][0] += up_rate * M[i-1][last_pos][1] * up_trans * p_trans[pull];
                    M[i][j][0] += M[i-1][last_pos][3] * p_trans[pull];
                    M[i][j][0] += stander_trans * (1.0-up_rate) * M[i-1][last_pos][0] * p_trans[pull];
                    M[i][j][0] += stander_trans * (1.0-up_rate) * M[i-1][last_pos][1] * p_trans[pull];
                    M[i][j][0] += M[i-1][last_pos][2] * up_trans * p_trans[pull];
                }
                //抽到不想要UP  命定值为1
                M[i][j][1] += up_rate * M[i][last_pos][0] * (1.0-up_trans) * p_trans[pull];
                M[i][j][1] += stander_other * (1.0-up_rate) * M[i][last_pos][0] * p_trans[pull];
                //抽到了常驻    命定值为1
                M[i][j][2] += stander_notup * (1.0-up_rate) * M[i][last_pos][0] * p_trans[pull];
                //             命定值为2
                M[i][j][3] += up_rate * M[i][last_pos][1] * (1.0-up_trans) * p_trans[pull];
                M[i][j][3] += stander_other * (1.0-up_rate) * M[i][last_pos][1] * p_trans[pull];
                M[i][j][3] += stander_notup * (1.0-up_rate) * M[i][last_pos][1] * p_trans[pull];
                M[i][j][3] += M[i][last_pos][2] * (1.0-up_trans) * p_trans[pull];
            }
        }
    }

    /*结果提取部分*/
    int temp_pos;
    for(i=0; i<(item_num+1)*(calc_pull+1); i++)
        ans[i] = 0;
    //返回恰好在某抽抽到的概率
    for(i=1; i<=item_num; i++)
        for(j=1; j<=calc_pull; j++)
        {
            temp_pos = i * (calc_pull+1) + j;
            ans[temp_pos] = M[i][j][0];
        }
    return;
}

/*常驻池DP*/
void APICALL GI_stander_DP(
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
)
{
    int i,j,k,pull;
    //DP数组声明
    double ***M, ***O;
    double* temp_storage_M = malloc((item_num+1) * (calc_pull+1) * (hit_pos+1) * sizeof(double));
    double* temp_storage_O = malloc((item_num+1) * (calc_pull+1) * (hit_pos+1) * sizeof(double));
    for(i=0; i<(item_num+1)*(calc_pull+1)*(hit_pos+1); i++)
    {
        temp_storage_M[i] = 0;
        temp_storage_O[i] = 0;
    }
    M = build_3D_index(temp_storage_M, item_num+1, calc_pull+1, hit_pos+1);
    O = build_3D_index(temp_storage_O, item_num+1, calc_pull+1, hit_pos+1);
    
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
    if(last_type == 0)  //上个物品是本类
        M[0][0][type_state] = 1;
    else                //上个物品是异类
        O[0][0][type_state] = 1;

    int last_pos;       //开始转移概率位置
    int fix_pull;       //修正非0开始的平稳参数
    double p_trans;     //恰好在本抽抽到概率
    double p_get;       //常驻本类所有物品中得到想要物品的概率
    double p_not_get;   //算法需要值
    double p_hit;       //异类转移到本类别的概率
    
    /*DP部分*/
    for(i=0; i<=item_num; i++)          //从零开始，用于记录先歪再抽的情况
    {
        //设定转移到想要物品概率
        p_get = 1.0/(double)stander_num;
        p_not_get = (double)(stander_num-1)/(double)stander_num;
        if(collect_all)                 //如果是考虑收集齐全的情况
        {
            if(i)
            {
                p_get = (double)(stander_num-i+1)/(double)stander_num;
                p_not_get = (double)(i)/(double)stander_num;
            }
            else
            {
                p_get = 1.0;
                p_not_get = 0.0;
            }
        }
        for(j=1; j<=calc_pull; j++)     //计算抽到j抽时候的情况
        {
        /*
        //编译加入并行优化
        #ifdef OPENMP_PARALLEL
        #pragma omp parallel for
        #endif
        */
            for(k=0; k<=hit_pos; k++)   //枚举另一类物品已经多久没抽到了
            {
                for(pull=1; pull<=(pity_pos>j?j:pity_pos); pull++)
                {
                    //等级保底
                    last_pos = j-pull;  //上个物品位置
                    fix_pull = pull;
                    if(last_pos)        //非从零开始
                        p_trans = p_normal[pull];
                    else                //从零开始
                    {
                        p_trans = p_first[pull];
                        fix_pull = pull + pull_state;
                    }
                        
                    //类别保底 以下参数用于不同类别转移
                    if(pull+k > hit_pos)
                        p_hit = 1;
                    else
                        p_hit = hit_p[pull+k];
                    
                    //状态转移
                    //本类到本类状态转移
                    if(k-pull >= 0)
                    {
                        //抽到了
                        if(i)
                            M[i][j][k] += M[i-1][last_pos][k-pull] * p_trans * (1.0-hit_p[k]) * p_get;
                        //没抽到
                        M[i][j][k] += M[i][last_pos][k-pull] * p_trans * (1.0-hit_p[k]) * p_not_get;
                    }
                    //异类到本类的转移
                    if(i)
                        M[i][j][fix_pull] += O[i-1][last_pos][k] * p_trans * p_hit * p_get;
                    M[i][j][fix_pull] += O[i][last_pos][k] * p_trans * p_hit * p_not_get;
                    //异类到异类的转移
                    if(k-pull >= 0)
                        O[i][j][k] += O[i][last_pos][k-pull] * p_trans * (1.0-hit_p[k]);
                    //本类到异类的转移
                    O[i][j][fix_pull] += M[i][last_pos][k] * p_trans * p_hit;
                }
            }
        }
    }
    /*结果提取部分*/
    int temp_pos;
    for(i=0; i<(item_num+1)*(calc_pull+1); i++)
        ans[i] = 0;
    //返回恰好在某抽抽到的概率
    for(i=1; i<=item_num; i++)          //抽到了i个物品
    {
        //设定转移到想要物品概率
        p_get = 1.0/(double)stander_num;
        if(collect_all)                 //如果是考虑收集齐全的情况
        {
            if(i)
                p_get = (double)(stander_num-i+1)/(double)stander_num;
            else
                continue;
        }
        for(j=1; j<=calc_pull; j++)     //计算抽到j抽时候的情况
        {
        /*
        //编译加入并行优化
        #ifdef OPENMP_PARALLEL
        #pragma omp parallel for
        #endif
        */
            for(k=0; k<=hit_pos; k++)      //枚举另一类物品已经多久没抽到了
            {
                for(pull=1; pull<=(pity_pos>j?j:pity_pos); pull++)
                {
                    //等级保底
                    last_pos = j-pull;  //上个物品位置
                    if(last_pos)        //非从零开始
                        p_trans = p_normal[pull];
                    else                //从零开始
                        p_trans = p_first[pull];
                    //跨类别保底
                    if(pull+k > hit_pos)
                        p_hit = 1;
                    else
                        p_hit = hit_p[pull+k];
                    
                    //提取结果
                    temp_pos = i * (calc_pull+1) + j;
                    if(k-pull >= 0)
                        ans[temp_pos] += M[i-1][last_pos][k-pull] * p_trans * (1.0-hit_p[k]) * p_get;
                    ans[temp_pos] += O[i-1][last_pos][k] * p_trans * p_hit * p_get;
                }
            }
        }
    }
    return;
}