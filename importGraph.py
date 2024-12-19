import json
import os
from py2neo import Graph, Node, Relationship
import pandas as pd
import streamlit as st


def loadVariableInfo():
    # Get cache data
    file_name = "data_cache.json"

    if os.path.exists(file_name) and os.stat(file_name).st_size > 0:
        try:
            with open(file_name, "r", encoding="utf-8") as f:
                json_data = json.load(f)

                for entry in json_data:
                    cached_data.append(entry)

            print("Loaded data as dict:", cached_data)

        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
    else:
        print(f"File '{file_name}' is empty or does not exist.")


def CreateNode(df, dict):

    nodes = []
    label = dict["Node Name"]
    propertyKey = dict["Property Key"]
    del dict["Node Name"]
    del dict["Property Key"]

    for _, row in df.iterrows():

        properties = {value: row[key] for key, value in dict.items()}

        node = Node(label, **properties)
        nodes.append(node)
    return label,propertyKey, nodes


def importGraph(graph, df, dicts):
    if len(dicts) == 1:
        label, propertyKey, curNodes = CreateNode(df,dicts[0])
        for node in curNodes:
            graph.merge(node, label, dicts[0][propertyKey])
    for i in range(len(dicts) - 1):
        relationship = dicts[i]["Relation"]
        del dicts[i]["Relation"]
        label1, propertyKey1, curNodes = CreateNode(df, dicts[i])
        label2, propertyKey2, nextNodes = CreateNode(df, dicts[i+1])
        n = len(curNodes)
        for j in range(n):
            relation = Relationship(curNodes[j], relationship, nextNodes[j])
            graph.merge(curNodes[j], label1, dicts[i][propertyKey1])
            graph.merge(nextNodes[j], label2, dicts[i+1][propertyKey2])
            graph.merge(relation)


cached_data = []
# Connect to Neo4j Database
g = Graph(st.secrets["NEO4J_URI"], auth=(st.secrets["NEO4J_USERNAME"], st.secrets["NEO4J_PASSWORD"]))

path = pd.read_csv("/Users/sesamekiller/Desktop/University_Info.csv")


def startImport():
    loadVariableInfo()
    importGraph(g, path, cached_data)


if __name__ == "__main__":
    loadVariableInfo()
    startImport()

