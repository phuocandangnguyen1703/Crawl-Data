import time
import pandas as pd

df_node_old = pd.read_csv('./link_node_stack_v2.csv',encoding='utf-8')
df_edge_old = pd.read_csv('link_edges_stack_v2.csv', encoding='utf-8')

df_node_new = pd.read_csv('./StackOverFlow_Node_v3.csv',encoding='utf-8')
df_edge_new = pd.read_csv('./Egdes_Stack_v3.csv',encoding='utf-8')

merged_df_node = pd.concat([df_node_new, df_node_old])
# Drop duplicate rows from the merged dataframe
merged_df_node = merged_df_node.drop_duplicates()
# Reset the index of the merged dataframe
merged_df_node = merged_df_node.reset_index(drop=True)
merged_df_edge = pd.concat([df_edge_old, df_edge_new], ignore_index=True)
result_df = merged_df_edge.groupby(['source', 'target'], as_index=False)['value'].sum()

merged_df_node.to_csv(r'./link_node_stack_v2.csv', header=True, encoding="utf-8")
result_df.to_csv(r'./link_edges_stack_v2.csv', header=True, encoding="utf-8")
