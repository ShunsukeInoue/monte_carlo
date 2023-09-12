import streamlit as st
import random
import numpy as np
import matplotlib.pyplot as plt

st.header("モンテカルロシュミレーター")
betting_theory = st.selectbox("ベッティング方法を選択してください", ["-", "マーチンゲール法"], 0)
perpose = st.selectbox("目的を選択してください", ["-", "資金の動きをシュミレーションする", "破産する確率を計算する"], 0)
st.write("----------------------------------------")
if betting_theory == "マーチンゲール法":
    if perpose == "資金の動きをシュミレーションする":
        """
        ```
        「説明」
        マーチンゲール法とは、負けたら当たるまで掛け金を倍にしていくベッティング方法です。
        この方法における資金の動きをシュミレーションします。
        シュミレーションは破産するまで繰り返されます。
        ```
        """
        st.write("")
        st.write("以下の設定値を入力して実行を押してください。")
        st.write("※実行を繰り返し押すことで、何度もシュミレーションできます。")
        p = float(st.text_input("賭けた場所が当たる確率", 0.48))
        odds = float(st.text_input("賭けた場所のオッズ", 2.02))
        bank_role = int(st.text_input("初期資金", 3000))
        first_bet = int(st.text_input("ベット額初期値", 3))
        bet = 0
        lose_count = 0
        bank_role_history = []
        if st.button("実行"):
            bank_role_history.append(bank_role)
            while True:
                if lose_count != 0:
                    bet = bet * 2
                else:
                    bet = first_bet

                if bank_role < 0:
                    break

                bank_role -= bet
                if random.random() < p:
                    bank_role += bet * odds
                    lose_count = 0

                else:
                    lose_count += 1
                bank_role_history.append(bank_role)
            st.line_chart(bank_role_history)
            plt.plot(bank_role_history, label="Bank Role Over Time")
            plt.xlabel("Number of Bets")
            plt.ylabel("Bank Role")
            plt.legend()
            plt.show()

    if perpose == "破産する確率を計算する":
        st.write("準備中")
