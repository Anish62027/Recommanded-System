import streamlit as st
import pickle
import numpy as np

# Load the required files
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# Function to recommend books
def recommend_books(book_title):
    try:
        index = np.where(pt.index == book_title)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

        recommendations = []
        for i in similar_items:
            item = {}
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item['title'] = list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values)[0]
            item['author'] = list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values)[0]
            item['image'] = list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values)[0]
            
            # Safely access 'avg_rating'
            item['rating'] = temp_df['avg_rating'].values[0] if 'avg_rating' in temp_df.columns else "N/A"
            recommendations.append(item)

        return recommendations
    except IndexError:
        return []

# Streamlit app
st.title("Book Recommendation System")

# Navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Choose a section:", ["Popular Books", "Book Recommendations"])

if options == "Popular Books":
    st.header("Popular Books")
    
    cols = st.columns(3)  # Create 3 columns for displaying books in a row
    for index, book in popular_df.iterrows():
        with cols[index % 3]:  # Distribute books across columns
            st.image(book['Image-URL-M'], width=120)
            st.markdown(f"**{book['Book-Title']}**")
            st.markdown(f"*by {book['Book-Author']}*")
            avg_rating = book.get('avg_rating', "N/A")
            num_ratings = book.get('num_ratings', "N/A")
            st.markdown(f"⭐ {avg_rating} ({num_ratings} votes)")
            st.write("---")

elif options == "Book Recommendations":
    st.header("Get Book Recommendations")
    
    method = st.radio("How would you like to search?", ["By typing a book title", "By selecting a book from the list"])
    
    if method == "By typing a book title":
        user_input = st.text_input("Enter a book title:")
        if st.button("Get Recommendations"):
            if user_input:
                recommendations = recommend_books(user_input)
                if recommendations:
                    st.subheader("Recommended Books")
                    for rec in recommendations:
                        st.image(rec['image'], width=100)
                        st.write(f"**{rec['title']}** by {rec['author']}")
                        st.write(f"⭐ {rec['rating']}")
                else:
                    st.error("No recommendations found. Please check the book title and try again.")
            else:
                st.warning("Please enter a book title to get recommendations.")

    elif method == "By selecting a book from the list":
        book_options = list(pt.index)
        selected_book = st.selectbox("Choose a book from the list:", book_options)
        if st.button("Get Recommendations"):
            if selected_book:
                recommendations = recommend_books(selected_book)
                if recommendations:
                    st.subheader("Recommended Books Based on Your Preference")
                    for rec in recommendations:
                        st.image(rec['image'], width=100)
                        st.write(f"**{rec['title']}** by {rec['author']}")
                        st.write(f"⭐ {rec['rating']}")
                else:
                    st.error("No recommendations found. Please try another book.")
            else:
                st.warning("Please select a book to get recommendations.")
