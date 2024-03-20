import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import seaborn as sns
import os
import pickle
import matplotlib.pyplot as plt
import pandas as pd
import sys
sys.path.append('../../main_code')  # 添加两级上级目录到sys.path中
import getTokenNumbers

def analyze_Codeflaws(prompt,experiment_index,experiment_model,rangeIndex,root_path):
    top1 = top3 = top5 = top10 = topNull = 0
    istop1=istop5=istop10=0
    err_list = []

    top1_list = set()
    top5_list = set()
    top10_list = set()
    # root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data/codeflaws/version"

    len_list = []
    # 200-300  -600  -900 -1200 1200+
    token_len_top1 = [0,0,0,0,0]
    token_len = [0,0,0,0,0]
    Codeflaws_Filter_Data = []
    with open("D:/私人资料/论文/大模型相关/大模型错误定位实证研究/LLM_In_Novice_Program_FL/LocalTest/main_code/evaluate/Codeflaws_Filter_Data.pkl", "rb") as f:
        Codeflaws_Filter_Data = pickle.load(f)

    Codeflaws_Length_Data = []
    process_num = 0

    for versionInt in range(1, 1544):
        istop1 = istop5 = istop10 = 0

        versionStr = "v" + str(versionInt);
        if versionStr not in Codeflaws_Filter_Data:
            print("跳过:"+versionStr)
            continue

        #在遍历达到一定个数后退出
        process_num +=1

        # print("processing: " + versionStr+" 第"+process_num+"个")
        if process_num>rangeIndex:
            break

        print("正在跑Codeflaws上的 " + experiment_model + " 实验： " + str(experiment_index) + " 的第 " + str(
            process_num) + " 个程序")

        print("processing: " + versionStr)
        # 数据目录
        # 输出的目录
        ans_path = os.path.join(root_path, versionStr, "test_data", experiment_model)
        ans_path = os.path.join(ans_path, str(experiment_index))
        top_N_path = os.path.join(ans_path, "topN.txt")
        code_location = os.path.join(root_path, versionStr, "test_data/defect_root/source/tcas.c_indexed.txt")
        with open(code_location, 'r', encoding='utf-8') as file:
            # 读取文件内容并保存到字符串中
            code = file.read()

        tokens = getTokenNumbers.get_openai_token_len(code, model="text-davinci-001")
        Codeflaws_Length_Data.append(tokens)
        if tokens < 300:
            token_len[0] += 1
        elif tokens < 600:
            token_len[1] += 1
        elif tokens < 900:
            token_len[2] += 1
        elif tokens < 1200:
            token_len[3] += 1
        else:
            token_len[4] += 1
        len_list.append(tokens)

        topN_str = 100
        try:
            with open(top_N_path, 'r') as file:
                topN_str = file.read()
        except:
            print("读取topN失败:", top_N_path)

            # err_list.append(versionInt)

        topN_Index = int(topN_str)
        # 处理topn数据，并统计每一个程序是top几
        if topN_Index <= 1:
            top1 += 1
            # istop1=1
            top1_list.add(versionInt)
            if tokens < 300:
                token_len_top1[0] += 1
            elif tokens < 600:
                token_len_top1[1] += 1
            elif tokens < 900:
                token_len_top1[2] += 1
            elif tokens < 1200:
                token_len_top1[3] += 1
            else:
                token_len_top1[4] += 1

        if topN_Index <= 3:
            top3 += 1
        if topN_Index <= 5:
            top5 += 1
            # istop5=1
            top5_list.add(versionInt)
        if topN_Index <= 10:
            top10 += 1
            # istop10=1
            top10_list.add(versionInt)
        else:
            topNull += 1
    # ans = [top1_list, top5_list, top10_list]
    # return ans
    # nums = [top1, top3, top5, top10]
    # with open("Codeflaws_Length_Data.pkl", 'wb') as file:
    #     pickle.dump(Codeflaws_Length_Data, file)
    return token_len,token_len_top1


def analyze_Condefects(experiment_index, model_name, rangeIndex,root_path):
    # root_path = "/root/autodl-tmp/data/ConDefects-main/Code/"
    top1 = top3 = top5 = top10 = topNull = 0
    # Condefects_Filter_Data = []
    top1_list = set()
    top5_list = set()
    top10_list = set()

    try:
        with open("D:/私人资料/论文/大模型相关/大模型错误定位实证研究/LLM_In_Novice_Program_FL/LocalTest/main_code/evaluate/Condefects_Filter_Data.pkl", 'rb') as file:
            Condefects_Filter_Data = pickle.load(file)
    except:
        print("Condefects_Filter_Data读取失败")
        jump_flag = False

    process_num = 0

    # 遍历文件夹中的所有内容
    questions = os.listdir(root_path)
    for question in questions:
        if process_num > rangeIndex:
            print("达到上线: " + str(rangeIndex))
            break
        question_path = os.path.join(root_path, question)

        # 检查是否为文件夹
        if os.path.isdir(question_path):
            # print(f'子文件夹: {contest_path}')
            try:
                java_path = os.path.join(question_path, "Java")
                questions = os.listdir(java_path)
                answers = os.listdir(java_path)
            except:
                print("列出JavaPath " + java_path + " 失败")
                continue
            for answer in answers:
                if answer not in Condefects_Filter_Data:
                    continue
                process_num += 1
                if process_num > rangeIndex:
                    print("达到上线: " + str(rangeIndex))
                    break

                # 数据目录
                # 输出的目录
                code_location = os.path.join(java_path, answer, "correctVersion.java")
                faulte_data_path = os.path.join(java_path, answer, "faultLocation.txt")
                ans_path = os.path.join(java_path, answer, model_name, str(experiment_index))
                top_N_path = os.path.join(ans_path, "topN.txt")

                topN_str = 100
                try:
                    with open(top_N_path, 'r') as file:
                        topN_str = file.read()
                except:
                    print("读取topN失败:", top_N_path)
                    # Condefects_Filter_Data = remove_element(Condefects_Filter_Data,answer)
                    # err_list.append(versionInt)
                    # continue

                topN_Index = int(topN_str)
                if topN_Index <= 1:
                    top1 += 1
                    top1_list.add(process_num)
                if topN_Index <= 3:
                    top3 += 1
                if topN_Index <= 5:
                    top5 += 1
                    top5_list.add(process_num)
                if topN_Index <= 10:
                    top10 += 1
                    top10_list.add(process_num)
                else:
                    topNull += 1

    # print("top1: ", top1)
    # print("top3: ", top3)
    # print("top5: ", top5)
    # print("top10: ", top10)
    # print("topNull: ", topNull)
    # total_Num = top10 + topNull
    #
    nums = [top1, top3, top5, top10]
    return nums

    # ans = [top1_list, top5_list, top10_list]
    # return ans

def test_Condefects(experiment_index,rangeIndex,model_name):
    root_path = "/root/autodl-tmp/data/ConDefects-main/Code/"
    top1=top3=top5=top10=topNull=0
    # Condefects_Filter_Data = []

    try:
        with open('Condefects_Filter_Data.pkl', 'rb') as file:
            Condefects_Filter_Data = pickle.load(file)
    except:
        print("Condefects_Filter_Data读取失败")
        jump_flag = False

    process_num = 0

    # 遍历文件夹中的所有内容
    questions = os.listdir(root_path)
    for question in questions:
        if process_num > rangeIndex:
            print("达到上线: " + str(rangeIndex))
            break
        question_path = os.path.join(root_path, question)

        # 检查是否为文件夹
        if os.path.isdir(question_path):
            # print(f'子文件夹: {contest_path}')
            try:
                java_path = os.path.join(question_path, "Java")
                questions = os.listdir(java_path)
                answers = os.listdir(java_path)
            except:
                print("列出JavaPath " + java_path + " 失败")
                continue
            for answer in answers:
                if answer not in Condefects_Filter_Data:
                    continue
                process_num+=1
                if process_num > rangeIndex:
                    print("达到上线: "+str(rangeIndex))
                    break

                #数据目录
                # 输出的目录
                code_location = os.path.join(java_path, answer, "correctVersion.java")
                faulte_data_path = os.path.join(java_path, answer, "faultLocation.txt")
                ans_path = os.path.join(java_path, answer, model_name, str(experiment_index))
                top_N_path = os.path.join(ans_path,"topN.txt")

                topN_str = 100
                try:
                    with open(top_N_path, 'r') as file:
                        topN_str = file.read()
                except:
                    print("读取topN失败:", top_N_path)
                    # Condefects_Filter_Data = remove_element(Condefects_Filter_Data,answer)
                    # err_list.append(versionInt)
                    # continue

                topN_Index = int(topN_str)
                if topN_Index<=1:
                    top1+=1
                if topN_Index<=3:
                    top3+=1
                if topN_Index<=5:
                    top5+=1
                if topN_Index<=10:
                    top10+=1
                else:
                    topNull+=1

    # with open("Condefects_Filter_Data.pkl", 'wb') as file:
    #     pickle.dump(Condefects_Filter_Data, file)
    print("top1: ",top1)
    print("top3: ", top3)
    print("top5: ", top5)
    print("top10: ", top10)
    print("topNull: ", topNull)
    total_Num = top10+topNull

    nums = [top1, top3, top5, top10,topNull]
    return nums
    # draw_pic(nums,total_Num)

    # data = pd.DataFrame({
    #     'TopN': ['top1', 'top3', 'top5', 'top10','top10+'],
    #     'Nums': [top1, top3, top5, top10,topNull]
    # })
    #
    # # 使用Seaborn绘制柱状图
    # plt.figure(figsize=(8, 6))
    # barplot=sns.barplot(x='TopN', y='Nums', data=data)
    #
    # # 在每个柱子上显示值
    # for p in barplot.patches:
    #     barplot.annotate(f'{int(p.get_height())}',
    #                      (p.get_x() + p.get_width() / 2., p.get_height()),
    #                      ha='center', va='center',
    #                      xytext=(0, 9),
    #                      textcoords='offset points')
    # plt.text(0, 200, f"total num:{total_Num}", fontsize=12, color='black')
    #
    # # 显示图形
    # plt.title('Top-N Analyze')
    # plt.show()

def draw_pic(Nums,total_Num):
    data = pd.DataFrame({
        'TopN': ['top1', 'top3', 'top5', 'top10', 'top10+'],
        'Nums': Nums
    })

    # 使用Seaborn绘制柱状图
    plt.figure(figsize=(8, 6))
    barplot = sns.barplot(x='TopN', y='Nums', data=data)

    # 在每个柱子上显示值
    for p in barplot.patches:
        barplot.annotate(f'{(p.get_height())}',
                         (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center',
                         xytext=(0, 9),
                         textcoords='offset points')
    # plt.text(0, 200, f"total num:{total_Num}", fontsize=12, color='black')

    # 显示图形
    plt.title('Top-N Analyze')
    plt.show()

def remove_element(arr, element):
    # Remove all occurrences of 'element' from 'arr'
    return [x for x in arr if x != element]

if __name__ == "__main__":
    # model_name="chatGlm3"
    # gpt-4
    # experiment_model = "gpt-3.5-turbo"

    # 画codeflaws上的
    title = "LLMs_lenth_evaluate_in_Codeflaws"
    root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data/codeflaws/version"
    gpt4_token_len,gpt4_token_len_top1 = analyze_Codeflaws("prompt", 1, "gpt-4", 503,root_path)
    gpt4_result = [round(a / b, 4) for a, b in zip(gpt4_token_len_top1, gpt4_token_len)]
    chatGlm3_token_len, chatGlm3_token_len_top1 = analyze_Codeflaws("prompt", 1, "chatGlm3", 503, root_path)
    chatGlm3_result = [round(a / b, 4) for a, b in zip(chatGlm3_token_len_top1, chatGlm3_token_len)]
    gpt3_5_token_len, gpt3_5_token_len_top1 = analyze_Codeflaws("prompt", 1, "gpt-3.5-turbo", 503, root_path)
    gpt3_5_result = [round(a / b, 4) for a, b in zip(gpt3_5_token_len_top1, gpt3_5_token_len)]
    root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data_2024_0313/codeflaws/version"
    llama_token_len, llama_token_len_top1 = analyze_Codeflaws("prompt", 1, "openbuddy-llama", 503, root_path)
    llama_result = [round(a / b, 4) for a, b in zip(llama_token_len_top1, llama_token_len)]
    codellama_token_len, codellama_token_len_top1 = analyze_Codeflaws("prompt", 1, "code-llama", 503, root_path)
    codellama_result = [round(a / b, 4) for a, b in zip(codellama_token_len_top1, codellama_token_len)]

    # ans_gpt3_5 = analyze_Codeflaws("prompt", 1, "gpt-3.5-turbo", 503,root_path)
    # ans_chatGlm3 = analyze_Codeflaws("prompt", 1, "chatGlm3", 503,root_path)
    # root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data_2024_0313/codeflaws/version"
    # ans_llama = analyze_Codeflaws("prompt", 1, "openbuddy-llama", 503, root_path)
    # ans_codellama = analyze_Codeflaws("prompt", 1, "code-llama", 503, root_path)

    with open("./"+title+".txt", 'w') as file:
        file.write("name:  top1 top3 top5 top10" + '\n')
        file.write("gpt4_result: "+str(gpt4_result)+'\n')
        file.write("gpt3_5_result: " + str(gpt3_5_result)+'\n')
        file.write("chatGlm3_result: " + str(chatGlm3_result)+'\n')
        file.write("llama_result: " + str(llama_result)+'\n')
        file.write("codellama_result: " + str(codellama_result)+'\n')
    print("over")

    # # 画condefects上的
    # title = "LLMs_in_Condefects"
    # root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data/ConDefects-main/Code"
    # ans_gpt4 = analyze_Condefects( 1, "gpt-4", 503, root_path)
    # ans_gpt3_5 = analyze_Condefects( 1, "gpt-3.5-turbo", 503, root_path)
    # ans_chatGlm3 = analyze_Condefects( 1, "chatGlm3", 503, root_path)
    # root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data_2024_0313/ConDefects-main/Code"
    # ans_llama = analyze_Condefects( 1, "openbuddy-llama", 503, root_path)
    # ans_codellama = analyze_Condefects( 1, "code-llama", 503, root_path)
    #
    #
    # with open("./"+title+".txt", 'w') as file:
    #     file.write("name:  top1 top3 top5 top10" + '\n')
    #     file.write("ans_gpt4: "+str(ans_gpt4)+'\n')
    #     file.write("ans_gpt3_5: " + str(ans_gpt3_5)+'\n')
    #     file.write("ans_chatGlm3: " + str(ans_chatGlm3)+'\n')
    #     file.write("ans_llama: " + str(ans_llama)+'\n')
    #     file.write("ans_codellama: " + str(ans_codellama)+'\n')
    # print("over")



