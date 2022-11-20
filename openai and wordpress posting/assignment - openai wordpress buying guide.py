import requests
import base64

from dotenv import load_dotenv
load_dotenv()

import os
import openai

api_endpoint = os.getenv("api_endpoint")
User_name = os.getenv("User_name")
Password = os.getenv("Password")
Credential = f"{User_name}:{Password}"
Token = base64.b64encode(Credential.encode("utf-8"))
Header = {"Authorization": f"Basic {Token.decode()}"}


file = open('keywords.txt')
keywords = file.readlines()
file.close()


for keyword in keywords:
    keyword = keyword.strip('\n')


    def intro_prompt(keyword):
        query = f'Write around 80 words about this "{keyword}"'
        return query

    def first_query_what(keyword):
        query = f'Write in details about "what is {keyword}"'
        return query


    def second_query_why(keyword):
        query = f'Write in details about "why and who needs the {keyword}"'
        return query


    def third_query_factors(keyword):
        query = f'Write in details about "things to consider when buying {keyword}"'
        return query


    def conclusion_prompt(keyword):
        query = f'Write around 100 words of "conclusion" about this {keyword}'
        return query


    def wp_paragraph(text):
        paragraph = f"<!-- wp:paragraph --><p>{text}</p><!-- /wp:paragraph -->"
        return paragraph


    def conclusion_heading(text):
        con_heading_two = f'<!-- wp:heading --><h2>{text}</h2><!-- /wp:heading -->'
        return con_heading_two


    def first_heading_question(keyword):
        first_heading = f'<!-- wp:heading --><h2>What is {keyword}</h2><!-- /wp:heading -->'
        return first_heading.title()


    def second_heading_question(keyword):
        second_heading = f'<!-- wp:heading --><h2>Why and who needs the {keyword}</h2><!-- /wp:heading -->'
        return second_heading.title()


    def third_heading_question(keyword):
        third_heading = f'<!-- wp:heading --><h2>things to consider when buying {keyword}</h2><!-- /wp:heading -->'
        return third_heading.title()


    def post_slugify(keyword):
        slug = keyword.strip().replace(' ', '-')
        return slug


    def buying_guide(my_prompt):
        openai.api_key = os.getenv("openai.api_key")
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=my_prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        openai_data = response.get("choices")[0].get("text").strip('\n')
        return openai_data


    title = f'how to buy best {keyword} in 2022 '

    intro_query = intro_prompt(keyword)
    first_question = first_query_what(keyword)
    second_question = second_query_why(keyword)
    third_question = third_query_factors(keyword)
    ending_query = conclusion_prompt(keyword)

    intro_answer = buying_guide(intro_query)
    question_ans_what = buying_guide(first_question)
    question_ans_why = buying_guide(second_question)
    question_ans_factors = buying_guide(third_question)
    ending_answer = buying_guide(ending_query)

    post_title = title.title()
    post_intro = wp_paragraph(intro_answer)
    post_first_heading = first_heading_question(keyword)
    ans_of_what = wp_paragraph(question_ans_what)
    post_second_heading = second_heading_question(keyword)
    ans_of_why = wp_paragraph(question_ans_why)
    post_third_heading = third_heading_question(keyword)
    ans_of_factors = wp_paragraph(question_ans_factors)
    post_conclusion_heading= conclusion_heading("Conclusion")
    conclusion_text = wp_paragraph(ending_answer)
    post_slug = post_slugify(keyword)

    categories = '253'

    wp_content = f'{post_intro},{post_first_heading},{ans_of_what},{post_second_heading},{ans_of_why},{post_third_heading},{ans_of_factors},{post_conclusion_heading}{conclusion_text}'


    def wp_posting(post_title, wp_content, post_slug, categories):
        api_url = api_endpoint
        data = {
            'title': post_title,
            'slug': post_slug,
            'content': wp_content,
            'categories': categories,
        }
        response = requests.post(api_url, headers=Header, data=data)
        print(response.status_code)

    wp_posting(post_title,wp_content,post_slug,categories)