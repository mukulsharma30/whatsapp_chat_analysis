import streamlit as st
import preprocessor,helper # import from preprocessor.py || to develop relation between app.py & preprocessor
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Chat analysis')

uploaded_file = st.sidebar.file_uploader("Choose a file")           # side bar on the browser
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()           # after this we can upload file
    data= bytes_data.decode('utf-8') # it will make data in string format || decode in utf-8
    # st.text(data)    it will show text format after
    df = preprocessor.preprocessor(data)
    
    # st.dataframe(df)      # to show the datafram || after this it will show text as datafram

    #fetch unique user
    user_list = df['user'].unique().tolist()   # it will add drop & drag box
    user_list.remove('group notification')   # remove notification as it is not user
    user_list.sort()                         # sort the user
    user_list.insert(0,'Overall')            # add overall word in drop down
    selected_user = st.sidebar.selectbox("Show Analysis",user_list)

    if st.sidebar.button("Show Analysis"):  # show analysis button will get add
        num_messages, words, num_media_messages, num_links= helper.fetch_stats(selected_user,df) # calling function
        st.title("Top Statistics of whatsapp chat")  # title will add after show analysis button


    # add 4 columns
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total messages")    # it will show Total messages column
            st.title(num_messages)         # when we add num message(number of messages

        with col2:
            st.header("Total words")
            st.title(words)

        with col3:
            st.header("Media shared")
            st.title(num_media_messages)

        with col4:
            st.header("Links shared")
            st.title(num_links)

    if selected_user == 'Overall':       # adding most busy user
        st.title("Most busy users")
        x, new_df = helper.most_busy_users(df)
        fig,ax = plt.subplots()

        col1, col2 = st.columns(2)
        with col1:
            ax.bar(x.index,x.values,color='green')
            ax.tick_params(axis='x', rotation=30)  # rotate the x axis
            st.pyplot(fig)

        with col2:
            st.dataframe(new_df)

    most_common_df = helper.most_common_words(selected_user,df)

    st.title("Max words")
    st.dataframe(most_common_df)


    fig,ax = plt.subplots()

    ax.bar(most_common_df[0],most_common_df[1],color='orange')
    plt.xticks(rotation= 'vertical' )
    st.title("Most common words")
    st.pyplot(fig)

    emoji_df = helper.emoji_helper(selected_user,df)
    st.title("Emoji analysis")

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(emoji_df)

    with col2:
        fig,ax = plt.subplots()
        ax.pie(emoji_df[1].head(),labels = emoji_df[0].head(),autopct = '%0.2f')
        st.pyplot(fig)

    st.title("Monthly Timeline Analysis")
    timeline = helper.monthly_timeline(selected_user,df)

    fig,ax = plt.subplots()  # for figure

    ax.plot(timeline['time'], timeline['message'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # daily timeline

    st.title("Daily Timeline Analysis")
    daily_timeline = helper.daily_timeline(selected_user,df)

    fig,ax = plt.subplots()

    #plt.figure(figsize=(18, 15))
    ax.plot(daily_timeline['only_date'], daily_timeline['message'],color='black')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    st.title("Activity Map")
    col1, col2 = st.columns(2)

    with col1:
        st.header("Most Busy Day")
        busy_day = helper.week_activity_map(selected_user,df)

        fig,ax = plt.subplots()
        ax.bar(busy_day.index,busy_day.values,color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    with col2:
        st.header("Most Busy Month")
        busy_month = helper.week_activity_map(selected_user, df)

        fig, ax = plt.subplots()
        ax.bar(busy_day.index, busy_month.values, color='magenta')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    st.title("Online Statistics")
    user_heatmap = helper.activity_heatmap(selected_user,df)
    fig,ax = plt.subplots()
    ax = sns.heatmap(user_heatmap,annot=True,cmap='Blues',fmt='g')  # post annot showing diff gheatmap
    st.pyplot(fig)

