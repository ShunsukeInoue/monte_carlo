import streamlit as st
import random
import numpy as np
import time
import mydictionary
import copy

st.header("モンテカルロシュミレーター")
betting_theory = st.selectbox(
    "ベッティング方法を選択してください",
    ["-", mydictionary.BETTING1, mydictionary.BETTING2, mydictionary.BETTING3],
    0,
)
perpose = st.selectbox(
    "目的を選択してください",
    ["-", mydictionary.PERPOSE1, mydictionary.PERPOSE2, mydictionary.PERPOSE3],
    0,
)
st.write("----------------------------------------")

if betting_theory == mydictionary.BETTING1:
    if perpose == mydictionary.PERPOSE1:
        """
        ```
        「説明」
        マーチンゲール法とは、負けたら当たるまで掛け金を倍にしていくベッティング方法です。
        この方法における資金の動きをシュミレーションします。
        シュミレーションは破産するまで繰り返されます。
        破産しなかった場合は、100万回の施行結果が表示されます。
        ```
        """
        st.write("")
        st.write("以下の設定値を入力して実行を押してください。")
        st.write("※実行を繰り返し押すことで、何度もシュミレーションできます。")
        p = st.number_input("賭ける場所が当たる確率", 0.0, 0.99, 0.48)
        odds = st.number_input("賭ける場所のオッズ", 0.0, value=2.02)
        first_bank_role = st.number_input("初期資金", 1, value=3000)
        first_bet = st.number_input("ベット額初期値", 1, value=3)

        if st.button("実行"):
            bet = 0
            lose_count = 0
            bank_role_history = []
            bank_role_history.append(first_bank_role)
            bank_role = first_bank_role
            for i in range(1000000):
                if lose_count != 0:
                    bet = bet * 2
                else:
                    bet = first_bet

                if bank_role <= 0:
                    break

                bank_role -= bet
                if random.random() < p:
                    bank_role += bet * odds
                    lose_count = 0

                else:
                    lose_count += 1
                bank_role_history.append(bank_role)
            st.line_chart(bank_role_history)

    if perpose == mydictionary.PERPOSE2:
        """
        ```
        「説明」
        マーチンゲール法とは、負けたら当たるまで掛け金を倍にしていくベッティング方法です。
        目標資金に到達するまでに破産する確率をシュミレーションします。
        ```
        """
        st.write("")
        st.write("以下の設定値を入力して実行を押してください。")
        st.write("※実行を繰り返し押すことで、何度もシュミレーションできます。")
        p = st.number_input("賭ける場所が当たる確率", 0.0, 0.99, 0.48)
        odds = st.number_input("賭ける場所のオッズ", 0.0, value=2.02)
        first_bank_role = st.number_input("初期資金", 1, value=3000)
        target_bank_role = st.number_input("目標資金", 1, value=4500)
        first_bet = st.number_input("ベット額初期値", 1, value=3)

        if st.button("実行"):
            lose_total = 0
            count = 10000
            latest_iteration = st.empty()
            bar = st.progress(0.0)
            for i in range(count):
                latest_iteration.text(f"計算中...({i * 100 / count}%)")
                bar.progress(i / count)
                bank_role = first_bank_role
                bet = 0
                lose_count = 0
                while True:
                    if lose_count != 0:
                        bet = bet * 2
                    else:
                        bet = first_bet

                    if bank_role <= 0:
                        lose_total += 1
                        break

                    bank_role -= bet
                    if random.random() < p:
                        bank_role += bet * odds
                        lose_count = 0
                        if bank_role >= target_bank_role:
                            break

                    else:
                        lose_count += 1
            st.write(f"{count}回実行して{lose_total}回破産しました。")

    if perpose == mydictionary.PERPOSE3:
        """
        ```
        「説明」
        マーチンゲール法とは、負けたら当たるまで掛け金を倍にしていくベッティング方法です。
        破産するまでの平均試行回数をシュミレーションします。
        100万回試行しても破産しなかった場合、100万回目に破産したとして計算します。
        ```
        """
        st.write("")
        st.write("以下の設定値を入力して実行を押してください。")
        st.write("※実行を繰り返し押すことで、何度もシュミレーションできます。")
        p = st.number_input("賭ける場所が当たる確率", 0.0, 0.99, 0.48)
        odds = st.number_input("賭ける場所のオッズ", 0.0, value=2.02)
        first_bank_role = st.number_input("初期資金", 1, value=3000)
        first_bet = st.number_input("ベット額初期値", 1, value=3)

        if st.button("実行"):
            count = 10000
            bet_count = 1000000
            bankruptcy_history = []
            latest_iteration = st.empty()
            bar = st.progress(0.0)
            for i in range(count):
                latest_iteration.text(f"計算中...({i * 100 / count}%)")
                bar.progress(i / count)
                bank_role = first_bank_role
                bet = first_bet
                lose_count = 0
                for j in range(bet_count):
                    if lose_count != 0:
                        bet = bet * 2
                    else:
                        bet = first_bet

                    if bank_role <= 0:
                        bankruptcy_history.append(j)
                        break

                    bank_role -= bet
                    if random.random() < p:
                        bank_role += bet * odds
                        lose_count = 0

                    else:
                        lose_count += 1

                    if j + 1 == bet_count:
                        bankruptcy_history.append(j + 1)

            st.write(
                f"この設定における破産するまでの平均試行回数は{np.array(bankruptcy_history).mean()}回でした。"
            )
            st.line_chart(bankruptcy_history)


if betting_theory == mydictionary.BETTING2:
    if perpose == mydictionary.PERPOSE1:
        """
        ```
        「説明」
        定額ベット法とは、毎回同じ金額をベットするベッティング方法です。
        この方法における資金の動きをシュミレーションします。
        シュミレーションは破産するまで繰り返されます。
        破産しなかった場合は、100万回の施行結果が表示されます。
        ```
        """
        st.write("")
        st.write("以下の設定値を入力して実行を押してください。")
        st.write("※実行を繰り返し押すことで、何度もシュミレーションできます。")
        p = st.number_input("賭ける場所が当たる確率", 0.0, 0.99, 0.48)
        odds = st.number_input("賭ける場所のオッズ", 0.0, value=2.02)
        first_bank_role = st.number_input("初期資金", 1, value=3000)
        first_bet = st.number_input("ベット額初期値", 1, value=3)

        if st.button("実行"):
            bank_role_history = []
            bank_role_history.append(first_bank_role)
            bank_role = first_bank_role
            for i in range(1000000):
                if bank_role <= 0:
                    break

                bank_role -= first_bet
                if random.random() < p:
                    bank_role += first_bet * odds

                bank_role_history.append(bank_role)
            st.line_chart(bank_role_history)

    if perpose == mydictionary.PERPOSE2:
        """
        ```
        「説明」
        定額ベット法とは、毎回同じ金額をベットするベッティング方法です。
        目標資金に到達するまでに破産する確率をシュミレーションします。
        ```
        """
        st.write("")
        st.write("以下の設定値を入力して実行を押してください。")
        st.write("※実行を繰り返し押すことで、何度もシュミレーションできます。")
        p = st.number_input("賭ける場所が当たる確率", 0.0, 0.99, 0.48)
        odds = st.number_input("賭ける場所のオッズ", 0.0, value=2.02)
        first_bank_role = st.number_input("初期資金", 1, value=3000)
        target_bank_role = st.number_input("目標資金", 1, value=4500)
        first_bet = st.number_input("ベット額初期値", 1, value=3)

        if st.button("実行"):
            lose_total = 0
            count = 10000
            latest_iteration = st.empty()
            bar = st.progress(0.0)
            for i in range(count):
                latest_iteration.text(f"計算中...({i * 100 / count}%)")
                bar.progress(i / count)
                bank_role = first_bank_role
                while True:
                    if bank_role <= 0:
                        lose_total += 1
                        break

                    bank_role -= first_bet
                    if random.random() < p:
                        bank_role += first_bet * odds
                        if bank_role >= target_bank_role:
                            break

            st.write(f"{count}回実行して{lose_total}回破産しました。")

    if perpose == mydictionary.PERPOSE3:
        """
        ```
        「説明」
        定額ベット法とは、毎回同じ金額をベットするベッティング方法です。
        破産するまでの平均試行回数をシュミレーションします。
        100万回試行しても破産しなかった場合、100万回目に破産したとして計算します。
        ```
        """
        st.write("")
        st.write("以下の設定値を入力して実行を押してください。")
        st.write("※実行を繰り返し押すことで、何度もシュミレーションできます。")
        p = st.number_input("賭ける場所が当たる確率", 0.0, 0.99, 0.48)
        odds = st.number_input("賭ける場所のオッズ", 0.0, value=2.02)
        first_bank_role = st.number_input("初期資金", 1, value=3000)
        first_bet = st.number_input("ベット額初期値", 1, value=3)

        if st.button("実行"):
            count = 10000
            bet_count = 1000000
            bankruptcy_history = []
            latest_iteration = st.empty()
            bar = st.progress(0.0)
            for i in range(count):
                latest_iteration.text(f"計算中...({i * 100 / count}%)")
                bar.progress(i / count)
                bank_role = first_bank_role
                bet = first_bet
                for j in range(bet_count):
                    if bank_role <= 0:
                        bankruptcy_history.append(j)
                        break

                    bank_role -= first_bet
                    if random.random() < p:
                        bank_role += first_bet * odds

                    if j + 1 == bet_count:
                        bankruptcy_history.append(j + 1)

            st.write(
                f"この設定における破産するまでの平均試行回数は{np.array(bankruptcy_history).mean()}回でした。"
            )
            st.line_chart(bankruptcy_history)


if betting_theory == mydictionary.BETTING3:
    if perpose == mydictionary.PERPOSE1:
        """
        ```
        「説明」
        モンテカルロ法とは、以下の操作を繰り返すベッティング方法です。
        ①初期配列を決める。例)[1, 2, 3]
        ②両端の数字を合計した金額をベットする。
        ③勝った場合、両端の数字を配列から消去する。
        ④負けた場合、ベットした金額を配列に追加する。
        ⑤配列から数字がなくなったら初期配列に戻す。
        この方法における資金の動きをシュミレーションします。
        シュミレーションは破産するまで繰り返されます。
        破産しなかった場合は、10万回の施行結果が表示されます。
        ```
        """
        st.write("")
        st.write("以下の設定値を入力して実行を押してください。")
        st.write("※実行を繰り返し押すことで、何度もシュミレーションできます。")
        p = st.number_input("賭ける場所が当たる確率", 0.0, 0.99, 0.48)
        odds = st.number_input("賭ける場所のオッズ(現在変更不可)", value=2, disabled=True)
        first_bank_role = st.number_input("初期資金", 1, value=3000)
        first_bet = st.text_input("初期配列(現在変更不可)", "1,2,3", disabled=True)

        if st.button("実行"):
            bet = 0
            bank_role_history = []
            first_monte_array = [1, 2, 3]
            current_monte_array = []
            bank_role_history.append(first_bank_role)
            bank_role = first_bank_role
            for i in range(1000000):
                if len(current_monte_array) == 0:
                    current_monte_array = copy.deepcopy(first_monte_array)
                    bet = current_monte_array[0] + current_monte_array[-1]

                elif len(current_monte_array) == 1:
                    bet = current_monte_array[0]

                else:
                    bet = current_monte_array[0] + current_monte_array[-1]

                if bank_role <= 0:
                    break

                bank_role -= bet
                if random.random() < p:
                    bank_role += bet * odds
                    if len(current_monte_array) == 1:
                        current_monte_array.pop(0)
                    else:
                        current_monte_array.pop(0)
                        current_monte_array.pop(-1)

                else:
                    current_monte_array.append(bet)

                bank_role_history.append(bank_role)
            st.line_chart(bank_role_history)

    if perpose == mydictionary.PERPOSE2:
        """
        ```
        「説明」
        モンテカルロ法とは、以下の操作を繰り返すベッティング方法です。
        ①初期配列を決める。例)[1, 2, 3]
        ②両端の数字を合計した金額をベットする。
        ③勝った場合、両端の数字を配列から消去する。
        ④負けた場合、ベットした金額を配列に追加する。
        ⑤配列から数字がなくなったら初期配列に戻す。
        目標資金に到達するまでに破産する確率をシュミレーションします。
        ```
        """
        st.write("")
        st.write("以下の設定値を入力して実行を押してください。")
        st.write("※実行を繰り返し押すことで、何度もシュミレーションできます。")
        p = st.number_input("賭ける場所が当たる確率", 0.0, 0.99, 0.48)
        odds = st.number_input("賭ける場所のオッズ(現在変更不可)", value=2, disabled=True)
        first_bank_role = st.number_input("初期資金", 1, value=3000)
        target_bank_role = st.number_input("目標資金", 1, value=4500)
        const = st.text_input("初期配列(現在変更不可)", "1,2,3", disabled=True)
        first_monte_array = [1, 2, 3]

        if st.button("実行"):
            lose_total = 0
            count = 10000
            latest_iteration = st.empty()
            bar = st.progress(0.0)
            for i in range(count):
                latest_iteration.text(f"計算中...({i * 100 / count}%)")
                bar.progress(i / count)
                bet = 0
                current_monte_array = []
                bank_role = first_bank_role
                while True:
                    if len(current_monte_array) == 0:
                        current_monte_array = copy.deepcopy(first_monte_array)
                        bet = current_monte_array[0] + current_monte_array[-1]

                    elif len(current_monte_array) == 1:
                        bet = current_monte_array[0]

                    else:
                        bet = current_monte_array[0] + current_monte_array[-1]

                    if bank_role <= 0:
                        lose_total += 1
                        break

                    bank_role -= bet
                    if random.random() < p:
                        bank_role += bet * odds
                        if len(current_monte_array) == 1:
                            current_monte_array.pop(0)
                        else:
                            current_monte_array.pop(0)
                            current_monte_array.pop(-1)
                        if bank_role >= target_bank_role:
                            break

                    else:
                        current_monte_array.append(bet)
            st.write(f"{count}回実行して{lose_total}回破産しました。")

    if perpose == mydictionary.PERPOSE3:
        """
        ```
        「説明」
        モンテカルロ法とは、以下の操作を繰り返すベッティング方法です。
        ①初期配列を決める。例)[1, 2, 3]
        ②両端の数字を合計した金額をベットする。
        ③勝った場合、両端の数字を配列から消去する。
        ④負けた場合、ベットした金額を配列に追加する。
        ⑤配列から数字がなくなったら初期配列に戻す。
        破産するまでの平均試行回数をシュミレーションします。
        100万回試行しても破産しなかった場合、100万回目に破産したとして計算します。
        ```
        """
        st.write("")
        st.write("以下の設定値を入力して実行を押してください。")
        st.write("※実行を繰り返し押すことで、何度もシュミレーションできます。")
        p = st.number_input("賭ける場所が当たる確率", 0.0, 0.99, 0.48)
        odds = st.number_input("賭ける場所のオッズ(現在変更不可)", value=2, disabled=True)
        first_bank_role = st.number_input("初期資金", 1, value=3000)
        const = st.text_input("初期配列(現在変更不可)", "1,2,3", disabled=True)
        first_monte_array = [1, 2, 3]

        if st.button("実行"):
            count = 10000
            bet_count = 1000000
            bankruptcy_history = []
            latest_iteration = st.empty()
            bar = st.progress(0.0)
            for i in range(count):
                latest_iteration.text(f"計算中...({i * 100 / count}%)")
                bar.progress(i / count)
                current_monte_array = []
                bank_role = first_bank_role
                bet = 0
                for j in range(bet_count):
                    if len(current_monte_array) == 0:
                        current_monte_array = copy.deepcopy(first_monte_array)
                        bet = current_monte_array[0] + current_monte_array[-1]

                    elif len(current_monte_array) == 1:
                        bet = current_monte_array[0]

                    else:
                        bet = current_monte_array[0] + current_monte_array[-1]

                    if bank_role <= 0:
                        bankruptcy_history.append(j)
                        break

                    bank_role -= bet
                    if random.random() < p:
                        bank_role += bet * odds
                        if len(current_monte_array) == 1:
                            current_monte_array.pop(0)
                        else:
                            current_monte_array.pop(0)
                            current_monte_array.pop(-1)

                    else:
                        current_monte_array.append(bet)

                    if j + 1 == bet_count:
                        bankruptcy_history.append(j + 1)

            st.write(
                f"この設定における破産するまでの平均試行回数は{np.array(bankruptcy_history).mean()}回でした。"
            )
            st.line_chart(bankruptcy_history)
