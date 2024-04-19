import os
import datetime

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Temp Title App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 데이터를 저장할 파일 경로
DATA_FILE = "reason_written_data.csv"

# CSV 파일 로드
file_path = 'portfolio_ym.csv'
data_ym = pd.read_csv(file_path)
file_path = 'portfolio_sw.csv'
data_sw = pd.read_csv(file_path)
# 두 데이터프레임의 'Name' 열을 합쳐서 리스트로 만듦
lst = list(data_ym['Name']) + list(data_sw['Name'])
# st.write(lst)
unique_name_set = set(lst)

# 데이터 프레임이 존재하지 않는 경우 빈 데이터 프레임 생성
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["종목명", "작성일자", "작성자", "매수근거", "삭제"])
    df.to_csv(DATA_FILE, index=False)

# 데이터 로드
df = pd.read_csv(DATA_FILE)

# 입력 폼을 생성하는 함수
def create_input_form_ym():
    lst = list(unique_name_set)
    lst = sorted(lst)
    종목명 = st.selectbox("종목명", options=lst)
    today = str(datetime.date.today())
    작성일자 = st.date_input("작성일자", datetime.date(int(today.split('-')[0]), int(today.split('-')[1]), int(today.split('-')[2])))
    작성자 = st.selectbox("작성자", options=['YM', 'SW'])
    매수근거 = st.text_area("매수근거")
    추가 = st.button("Add")
    return 종목명, 작성일자, 작성자, 매수근거, 추가

# 데이터를 추가하고 파일에 저장하는 함수
def add_data_ym(종목명, 작성일자, 작성자, 매수근거):
    global df
    new_row = {"종목명": 종목명, "작성일자": 작성일자, "작성자": 작성자, "매수근거": 매수근거, "삭제": False,}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# 데이터를 삭제하는 함수
def delete_data_ym(index_to_delete):
    global df
    df.drop(index_to_delete, inplace=True)
    df.to_csv(DATA_FILE, index=False)

# 메인 함수
def main():
    global df

    with st.sidebar:
        # 데이터 입력 폼
        종목명, 작성일자, 작성자, 매수근거, 추가 = create_input_form_ym()
        if 추가:
            add_data_ym(종목명, 작성일자, 작성자, 매수근거)
            st.success("데이터 추가 완료!")

    st.header("근거")
    test = st.data_editor(
        df,
        column_config={
            "삭제": st.column_config.CheckboxColumn(
                "삭제",
                default=False,
            )
        },
        # disabled=["종목명"],
        width=1000,
        hide_index=True,
    )

    series = test['삭제']
    # st.text(series)
    # st.text(type(series))

    try:
        true_indices = series[series].index
        # st.write(true_indices[0])

        if true_indices[0]:
            try:
                delete_data_ym(true_indices[0])
                st.warning(f"{true_indices[0] + 1}번째 행이 삭제되었습니다.")
                # Update the displayed DataFrame after deletion
                df = pd.read_csv(DATA_FILE)
            except Exception as e:
                st.write(e)

            if st.button('새로고침'):
                st.rerun()
    except:
        pass

if __name__ == "__main__":
    main()
