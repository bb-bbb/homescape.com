# 월 단위로 변환
df['year_month'] = df['order_date'].dt.to_period('M')
df.head()

# 1. 그룹화 후 인덱스 초기화
monthly_sales = df.groupby(['category', 'year_month'])['total_sales'].sum().reset_index()
# 'category','year_month가 그룹화 기준이라서 인덱스로 설정됨
# 'category','year_month'는 행을 구분하는 기준이지 일반적 칼럼X
# 엑셀형식으로 바꾸기
# reset_index :(인덱스->칼럼) 'category','year_month'가 컬럼으로 들어가고 인덱스는 0부터 시작하는 숫자인덱스로 초기화

# 2. year_month를 datetime으로 변환(시계열 정렬용)
monthly_sales['year_month_dt'] = monthly_sales['year_month'].dt.to_timestamp()
# matplotlib-seaborn 같은 시각화도구는 x축에 datetime타입 넣으면 자동으로 시간순서대로 정렬->날짜포맷 예쁘게 표시
# to_timestamp(): period 기간 -> datetime(정확한 날짜형)

# x축에 '월'이름 표시
# 월 이름 추출(예 jan,Feb,Mar)
monthly_sales['month_label'] = monthly_sales['year_month_dt'].dt.strftime('%b')

# 3. 라인플롯 그리기
plt.figure(figsize=(12,6))
ax = sns.lineplot(data=monthly_sales, x='year_month_dt', y='total_sales', hue='category', marker='o')

# <중요> :oct을 x축에 양끝시작으로 고정하기
ax.set_xlim(pd.Timestamp('2023-10-01'), pd.Timestamp('2025-10-01'))

# 3. x축 설정: 3개월 간격으로 영어 월 표시
xticks = pd.date_range(start=monthly_sales['year_month_dt'].min(),
                       end=monthly_sales['year_month_dt'].max(),
                       freq='3MS')
xticks = pd.date_range(start='2023-10-01', end='2025-10-01', freq='3MS')

# date.strftime('%b') : 날짜에서 영어 월 이름 추출
# date.strftime('%b %y') : 날짜에서 영어 월 + 연도 추출
# 해당 날짜가 1월이면 월+연도 추출하고 그외면 월만 표시
# for date in xticks : xticks 리스트에 있는 날짜들 하나씩 반복

# 라벨 설정: Jan이면 "Jan", 나머지는 월 이름만
xtick_labels = [date.strftime('%b') for date in xticks]

# 조정: 시작날짜를 가장 가까운 과거 10월로 조정
plt.xticks(ticks=xticks, labels=xtick_labels)

plt.title('카테고리별 월별 매출액', fontsize=16)
plt.xlabel('월', fontsize=12)
plt.ylabel('매출액', fontsize=12)
plt.xticks(rotation=0)

# 기존 x축 격자선 완전히 끄기
ax.grid(False, axis='x')

# ⬇️ 여기만 추가하면 됩니다!
for date in xticks:
    if date.month == 1:
        ax.text(date, -0.06, date.strftime('%Y'),
                transform=ax.get_xaxis_transform(),
                ha='center', va='top', fontsize=12)
        ax.axvline(x=date, color='#D3D3D3', linestyle='-', linewidth=0.8)

plt.tight_layout()

# 마지막: 카테고리 사이즈 줄이기
plt.legend(title='카테고리', fontsize=9, title_fontsize=11)

# 그래프 바깥쪽 두껍게
[ax.spines[side].set_color('black') for side in ['top', 'bottom', 'left', 'right']]

# X축 눈금선 바깥쪽으로 표시
ax.tick_params(axis='x', direction='out', length=6, width=1.2, color='black')

# Y축 눈금선 바깥쪽으로 표시
ax.tick_params(axis='y', direction='out', length=6, width=1.2, color='black')

plt.show()
