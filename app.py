import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import helper
import preprocessor

st.title("Instructions")
st.header("1. Upload the Exported Chat File (in txt). [make sure you use 24hr format]")
st.header("2. Select the user for showing stats particular to that user")
st.header("3. Click the Show Analysis Button to view the stats")

st.sidebar.title("Whatsapp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file.\nGo to Chat -> Menu (top right) -> more options -> Export Chat -> without media.\nUpload the chat file(.txt) here")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetching unique users
    users_list = df['user'].unique().tolist()
    users_list.remove('group_notifications')

    users_list.sort()
    users_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show Analysis With Respect to user:", users_list)

    if st.sidebar.button("Show Analysis"):
        st.markdown("""---""")
        st.title("\n\nTop Statistics")

        num_messages, words, num_media_messages, links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media")
            st.title(num_media_messages)
        with col4:
            st.header("Total Links")
            st.title(links)

        # finding the busiest user in the chat
        if selected_user == 'Overall':
            st.markdown("""---""")
            st.title("\n\nMost Active Users")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='teal')
                plt.xticks(rotation='vertical')
                plt.xlabel("User")
                plt.ylabel("Messages")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # monthly messages timeline
        st.markdown("""---""")
        st.title("\n\nMonthly Messages Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='red')
        plt.xticks(rotation='vertical')
        plt.xlabel("Month-Year")
        plt.ylabel("Messages")
        st.pyplot(fig)

        # daily messages timeline
        st.markdown("""---""")
        st.title("\n\nDaily Messages Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(daily_timeline['date_num'], daily_timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        plt.xlabel("Month-Year")
        plt.ylabel("Messages")
        st.pyplot(fig)

        # message frequency analysis
        st.markdown("""---""")
        st.title("\n\nMessage Trends Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.header("Weekdays Trend")
            busy_day = helper.weekly_analysis(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='violet')
            plt.xticks(rotation='vertical')
            plt.xlabel("Weekday")
            plt.ylabel("Messages")
            st.pyplot(fig)
        with col2:
            st.header("Monthly Trend")
            busy_month = helper.monthly_analysis(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            plt.xlabel("Month")
            plt.ylabel("Messages")
            st.pyplot(fig)

        # periodic heatmap
        st.markdown("""---""")
        st.title("\n\nHourly Heatmap")
        heat_map = helper.periodic_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(heat_map)
        st.pyplot(fig)

        # most common 25 words
        st.markdown("""---""")
        most_common_df = helper.most_common_words(selected_user, df)
        st.title('\n\n20 Most Used Words')
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        plt.xlabel("Frequency")
        plt.ylabel("Message")
        st.pyplot(fig)
        # st.dataframe(most_common_df)

        # most common emojis
        st.markdown("""---""")
        most_emoji_df = helper.most_common_emojis(selected_user, df)
        st.title("\n\nMost Used Emojis")
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(most_emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(most_emoji_df['Count'],  autopct="%0.2f%%", radius=1.5)
            plt.pie([1], radius=0.5, colors='white')
            st.pyplot(fig)
        # fig, ax = plt.subplots()
        # ax.pie(most_emoji_df[0], most_emoji_df[1])
        # st.pyplot(fig)

        st.markdown("""---""")
        st.title("\n\n\nThankyou for sharing your data. View your processed dataframe:")
        st.dataframe(df)

        st.text("\nMade by Tirth Shah 😉\n")