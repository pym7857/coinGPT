import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Temp Title App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

col1, col2 = st.columns(2)

# @st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def main():
    with st.sidebar:
        # 종목 수정/추가를 위한 입력 필드
        # st.subheader('Edit/Add Stock')
        selected_user = st.selectbox('Select User', options=['YM', 'SW'])
        selected_stock = st.text_input('Select Stock to Edit / Add', key='ym1').upper()
        quantity = st.number_input('Enter Your Amount ($)', min_value=0, key='ym2')
        # average_price = st.number_input('Enter Average Price ($)', min_value=1, key='ym3')

        # 수정/추가 버튼
        if st.button('Edit/Add Stock', key='ym4'):
            edit_or_add_stock(selected_user, selected_stock, quantity)
    with col1:
        st.title('YM')
        
        # 포트폴리오 파일 로드
        FILE_NAME = 'portfolio_ym.csv'
        portfolio = load_portfolio(FILE_NAME)
        
        # 포트폴리오에서 종목별 금액 계산
        # portfolio['Amount'] = portfolio['Quantity'] * portfolio['Average Price']
        
        # 종목별 금액을 사용하여 원 그래프 그리기
        draw_pie_chart(portfolio)

        # 포트폴리오 다운로드
        csv = convert_df(portfolio)
        st.download_button(
            key="ym",
            label="Download data as CSV",
            data=csv,
            file_name='portfolio_ym.csv',
            mime='text/csv',
        )

    with col2:
        st.title('SW')
        
        # 포트폴리오 파일 로드
        FILE_NAME = 'portfolio_sw.csv'
        portfolio = load_portfolio(FILE_NAME)
        
        # 포트폴리오에서 종목별 금액 계산
        # portfolio['Amount'] = portfolio['Quantity'] * portfolio['Average Price']
        
        # 종목별 금액을 사용하여 원 그래프 그리기
        draw_pie_chart(portfolio)

        # 포트폴리오 다운로드
        csv = convert_df(portfolio)
        st.download_button(
            key="sw",
            label="Download data as CSV",
            data=csv,
            file_name='portfolio_sw.csv',
            mime='text/csv',
        )

def load_portfolio(FILE_NAME):
    """
    포트폴리오 파일을 로드하는 함수
    """
    try:
        portfolio = pd.read_csv(FILE_NAME)
    except FileNotFoundError:
        portfolio = pd.DataFrame(columns=['Name', 'Quantity'])
    return portfolio

def edit_or_add_stock(selected_user, selected_stock, quantity):
    """
    선택한 종목을 수정하거나 새로운 종목을 추가하는 함수
    """
    # User에 맞게 파일 가져오기
    FILE_NAME = ''
    if selected_user == 'YM':
        FILE_NAME = 'portfolio_ym.csv'
    else:
        FILE_NAME = 'portfolio_sw.csv'

    # 포트폴리오 파일 로드
    portfolio = load_portfolio(FILE_NAME)

    # edit/add 로직
    if selected_stock in portfolio['Name'].values:
        # 선택한 종목이 이미 포트폴리오에 있는 경우 수정
        if quantity == 0:
            
            portfolio = portfolio[portfolio['Name'] != selected_stock]
        else:
            portfolio.loc[portfolio['Name'] == selected_stock, ['Quantity']] = quantity
    else:
        # 선택한 종목이 포트폴리오에 없는 경우 추가
        new_stock = pd.DataFrame({'Name': [selected_stock], 'Quantity': [quantity]})
        portfolio = pd.concat([portfolio, new_stock], ignore_index=True)
    portfolio = portfolio.drop_duplicates().reset_index(drop=True)
    if not portfolio.empty:
        st.write(portfolio)
        if not portfolio.empty:
            portfolio.to_csv(FILE_NAME, index=False)
            st.success('Portfolio saved successfully.')
        else:
            st.warning('No data to save.')
    else:
        st.write('No stocks added yet.')

def generate_pastel_color():
    """
    파스텔톤의 랜덤한 색상을 생성하는 함수
    """
    # RGB 값의 범위를 0.5 ~ 1 사이로 설정하여 파스텔톤 색상 생성
    r = np.random.uniform(0.5, 1)
    g = np.random.uniform(0.5, 1)
    b = np.random.uniform(0.5, 1)
    return (r, g, b)

def draw_pie_chart(portfolio):
    """
    포트폴리오를 바탕으로 원 그래프를 그리는 함수
    """
    if not portfolio.empty:
        labels = portfolio['Name'].tolist()
        amounts = portfolio['Quantity'].tolist()
        # colors = np.random.rand(len(amounts), 3)
        colors = [generate_pastel_color() for _ in range(len(amounts))]
        
        fig, ax = plt.subplots()
        # ax.pie(amounts, labels=labels, autopct='%1.1f%%', colors=colors)
        patches, texts, autotexts = ax.pie(amounts, labels=labels, autopct='%1.1f%%', colors=colors)
        ax.axis('equal')
        fig.patch.set_facecolor('none')  # 그래프 배경 투명하게 설정
        
        # 텍스트 색상을 흰색으로 설정
        for text in texts:
            text.set_color('white')

        # 숫자 텍스트만 검정색으로 설정
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontweight('bold')
        
        fig.legend(loc="upper left", labels=labels)

        st.pyplot(fig)

        # 전체 포트폴리오의 총 금액 계산
        total_portfolio_amount = portfolio['Quantity'].sum()
        st.write(f'Total Portfolio Amount: ${total_portfolio_amount:.2f}')
    else:
        st.write('No stocks added yet.')

if __name__ == '__main__':
    main()
