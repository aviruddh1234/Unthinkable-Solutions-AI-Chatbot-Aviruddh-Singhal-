import pandas as pd
import re
from config import FAQ_DATASET_PATH

class FAQSearch:
    """
    FAQ search functionality to find relevant answers from the dataset.
    """
    
    def __init__(self):
        """Initialize FAQ search by loading the dataset."""
        self.faq_data = self.load_faq_data()
    
    def load_faq_data(self):
        """
        Load FAQ data from CSV file.
        
        Returns:
            pandas.DataFrame: FAQ dataset
        """
        try:
            df = pd.read_csv(FAQ_DATASET_PATH)
            print(f"Loaded {len(df)} FAQs from {FAQ_DATASET_PATH}")
            return df
        except FileNotFoundError:
            print(f"FAQ dataset not found at {FAQ_DATASET_PATH}")
            return pd.DataFrame()
        except Exception as e:
            print(f"Error loading FAQ data: {e}")
            return pd.DataFrame()
    
    def search_faq(self, query):
        """
        Search for relevant FAQ based on user query.
        
        Args:
            query (str): User's question/query
            
        Returns:
            str: FAQ answer if found, empty string otherwise
        """
        if self.faq_data.empty:
            return ""
        
        query_lower = query.lower()
        best_match = None
        best_score = 0
        
        # Search through each FAQ entry
        for _, row in self.faq_data.iterrows():
            score = 0
            
            # Check question similarity
            question_words = row['question'].lower().split()
            query_words = query_lower.split()
            
            # Count word matches in question
            for q_word in query_words:
                for f_word in question_words:
                    if q_word in f_word or f_word in q_word:
                        score += 2
            
            # Check keyword matches
            if 'keywords' in row and pd.notna(row['keywords']):
                keywords = [k.strip().lower() for k in str(row['keywords']).split()]
                for keyword in keywords:
                    if keyword in query_lower:
                        score += 1
            
            # Check answer content for additional matches
            answer_words = str(row['answer']).lower().split()
            for q_word in query_words:
                for a_word in answer_words:
                    if q_word in a_word or a_word in q_word:
                        score += 0.5
            
            # Update best match if this score is higher
            if score > best_score:
                best_score = score
                best_match = row
        
        # Return answer if we found a good match (score > 1)
        if best_match is not None and best_score > 20:
            return best_match['answer']
        
        return ""
    
    def get_all_faqs(self):
        """
        Get all FAQ entries.
        
        Returns:
            list: List of FAQ dictionaries
        """
        if self.faq_data.empty:
            return []
        
        return self.faq_data.to_dict('records')
