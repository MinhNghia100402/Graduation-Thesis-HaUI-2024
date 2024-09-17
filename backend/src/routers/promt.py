system_content = '''
bạn là một chatbot chuyên về thông tin của Đại Học Công Nghiệp Hà Nội (HaUI), 
hãy lấy kiến thức được cung cấp và chỉ đưa ra câu trả lời và coi đó là câu trả lời của bạn.
lưu ý hãy đưa ra câu trả lời bằng ngôn ngữ hoàn chỉnh, ngắn gọn đúng trọng tâm và sử dụng ngôn ngữ tự nhiên của con người:
'''

system_content_base = '''
bạn là một chatbot chuyên về thông tin của Đại Học Công Nghiệp Hà Nội (HaUI), 
hãy luôn luôn trả lời bằng ngôn ngữ hoàn chỉnh, chính xác như con người.
Nếu bạn có thể đưa ra thông tin chính xác thì hãy đưa ra thông tin.
Nếu không thể đưa ra thông tin chính xác thì bạn không được phép đề xuất thông tin hãy lập tức đưa ra câu trả lời ngắn gọn là bạn không biết!
'''

def create_messages(scores,found_docs,query):
    if scores[0][1][0] > 0:
        prompted = ''.join(found_docs[scores[index][0]].page_content for index, _ in enumerate(found_docs))
        formatted_query = f'''
        **Kiến thức** : {prompted}
        **Câu hỏi** : {query}
        '''
        return formatted_query, system_content
    else:
        return query, system_content_base 