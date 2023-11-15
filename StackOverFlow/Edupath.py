import json
import pandas as pd
import networkx as nx
import warnings
warnings.filterwarnings('ignore')
from community import community_louvain

#import dữ liệu từ file csv
G = nx.Graph(day="EduPath") #Khởi tạo đồ thị

df_nodes = pd.read_csv('link_node_stack_v2.csv')
df_edges = pd.read_csv('link_edges_stack_v2.csv')

#Add Node và Add Edge
for index, row in df_nodes.iterrows():
    G.add_node(row['name'])

for index, row in df_edges.iterrows():
    G.add_weighted_edges_from([(row['source'], row['target'], row['value'])])

df_skill = pd.read_csv('Skill.csv')
def find_label(df, community):
    # Tính số lượng phần tử trong cộng đồng được chọn mà thuộc vào từng nhóm
    group_counts = df[df['Detail'].isin(community)]['Group'].value_counts()
    # Kiểm tra xem có nhóm nào có số lượng phần tử cao nhất
    if len(group_counts) > 0:
        max_count = group_counts.max()
        matching_groups = group_counts[group_counts == max_count].index.tolist()
        matching_value = {}
        for group in matching_groups:
            matching_value[group] = df[df['Group'] == group]['Detail'].tolist()
        common_values = set(list(matching_value.values())[0]).intersection(community)
        return matching_groups,common_values
    return None




def recommend_communities(user_nodes,community_graph):
    status =""
    messages = ""
    maintype = []
    percent = []
    tag = []
    courses=[]
    if len(user_nodes) < 2:
        messages = "error_input_skill_must_greater_than1."
        status = "Fail"
        return json.dumps({"status": status, "messages": messages})
    # Step 3: Apply Louvain algorithm on community graph

    partition_louvain_slpa = community_louvain.best_partition(community_graph)
    target_communities = []
    for community_id in set(partition_louvain_slpa.values()):
        nodes = [node for node, node_label in partition_louvain_slpa.items() if node_label == community_id]
        user_count = sum(node in nodes for node in user_nodes)
        if user_count > 0:
            user_percentage = (user_count / len(nodes)) * 100
            target_communities.append((community_id, nodes, user_percentage))

    # Sắp xếp các cộng đồng theo phần trăm giảm dần
    target_communities = sorted(target_communities, key=lambda x: x[2], reverse=True)

    # Tính tổng phần trăm ban đầu
    total_percentage = sum(user_percentage for _, _, user_percentage in target_communities[:len(target_communities)])

    # Tính tổng phần trăm sai số
    diff_percentage = 100 - total_percentage

    # Cập nhật phần trăm cho các cộng đồng
    updated_communities = []
    for i, (community_id, nodes, user_percentage) in enumerate(target_communities[:len(target_communities)]):
        updated_percentage = user_percentage + (user_percentage / total_percentage) * diff_percentage
        updated_communities.append((community_id, nodes, updated_percentage))

    # Sắp xếp lại các cộng đồng theo phần trăm đã cập nhật
    updated_communities = sorted(updated_communities, key=lambda x: x[2], reverse=True)

    # Xuất ra kết quả
    if updated_communities:
        # print("Dưới đây là các lộ trình phù hợp với bạn:")
        dominant_group = None
        for i, (community_id, nodes, user_percentage) in enumerate(updated_communities):
            # print("Mã cộng đồng: {}".format(community_id))
            # print("Các phần tử trong cộng đồng: {}".format(nodes))
            result = find_label(df_skill, nodes)
            matching_groups, common_values = result
            # tag.append(common_values)
            if matching_groups:
                # print("{}. Lộ trình {} (Độ phù hợp  {:.2f}%)".format(i + 1, matching_groups, user_percentage))
                messages = "Success."
                status = "Success"
                tag.append(list(common_values))
                maintype.append(matching_groups)
                percent.append(user_percentage)
            else:
                # print("Không tìm thấy nhãn dán phù hợp")
                messages = "error_cannot_have_roadmap."
                status = "Not success"
                maintype = ["FrontEnd", "BackEnd", "DevOps","Android","Blockchain","Flutter"]
        print("")
        for i in range(len(maintype)):
          course = {
              "maintype": maintype[i][0],
              "percent": str(percent[i]),
              "recommend": tag[i],
              "done": user_nodes
          }
          courses.append(course)
          result = {
              "status": status,
              "messages": messages,
              "courses": courses
          }
        # return json.dumps({"status": status, "messages": messages,"maintype": maintype, "percent": percent, "tag": common_values})
        return json.dumps({"result": result})
    else:
        messages = "error_cannot_have_roadmap."
        status = "Not success"
        maintype = ["FrontEnd", "BackEnd", "DevOps","Android","Blockchain","Flutter"]
        for i in range(len(maintype)):
          course = {
              "maintype": maintype[i],
          }
          courses.append(course)
          result = {
              "status": status,
              "messages": messages,
              "courses": courses
          }
        return json.dumps({"result": result})

user_node=["html","css","java"]
recommend_communities(user_node,G)