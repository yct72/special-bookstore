from click import option
import requests 
import streamlit as st

url = 'https://cloud.culture.tw/frontsite/trans/emapOpenDataAction.do?method=exportEmapJson&typeId=M'
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)
res = response.json()

def getAllBookstore():
    url = 'https://cloud.culture.tw/frontsite/trans/emapOpenDataAction.do?method=exportEmapJson&typeId=M'
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    res = response.json()
    return res

def getCountyOption(items):
    optionList = []
    for item in items:
        name = item['cityName']
        if name[:3] not in optionList:
            optionList.append(name[:3]) 
    return optionList

def getDistrictOption(items, target):
    optionList = []
    for item in items:
        name = item['cityName']
        if target not in name:
            continue
        name.strip()
        district = name[5:]
        if len(district) == 0: continue 
        if district not in optionList:
            optionList.append(district)
    return optionList

def getSpecificBookstore(items, county, districts):
    specificBookstoreList = []
    for item in items:
        name = item['cityName']
        if county not in name: continue
        for district in districts:
            if district not in name: continue
            specificBookstoreList.append(item)
    return specificBookstoreList


def getBookstoreInfo(items):
    expanderList = []
    for item in items:
        expander = st.expander(item['name'])
        expander.image(item['representImage'])
        expander.metric('hitRate', item['hitRate'])
        expander.subheader('Introduction')
        expander.write(item['intro'])
        expander.subheader('Address')
        expander.write(item['address'])
        expander.subheader('Open Time')
        expander.write(item['openTime'])
        expander.subheader('Email')
        expander.write(item['email'])
        expanderList.append(expander)
    return expanderList


def app():
    bookstoreList = getAllBookstore()
    countyOption = getCountyOption(bookstoreList)
    
    st.header('Special Bookstore')
    st.metric('Total bookstore', len(bookstoreList))
    county = st.selectbox('???????????????', countyOption)
    districtOption = getDistrictOption(bookstoreList, county)
    district = st.multiselect('???????????????', districtOption)

    specificBookstore = getSpecificBookstore(bookstoreList, county, district)
    num = len(specificBookstore)
    st.write(f'?????????{num}?????????')

    specificBookstore.sort(key = lambda item: item['hitRate'], reverse=True)
    bookstoreInfo = getBookstoreInfo(specificBookstore)


if __name__ == '__main__':
    app()