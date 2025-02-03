import pandas as pd 
import seaborn as sb 
import streamlit as st
import numpy as np 
import json
import os
import csv
import calendar
import sys 
import time
import warnings 
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import io
import requests
import datetime
import subprocess
import africastalking
import yfinance as yf
import openai
import os
import pyttsx3 as pt
from gtts import gTTS

from datetime import datetime, timedelta
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from dateutil.relativedelta import relativedelta
from streamlit_chat import message
from streamlit_folium import st_folium, folium_static
from dotenv import load_dotenv

load_dotenv()


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from model.ml_models import regression_model, future_prediction

openai.api_key = os.getenv("OPENAI_API_KEY")


africastalking.initialize(
    username='EMID',
    api_key = os.getenv("AT_API_KEY")
)

sms = africastalking.SMS
airtime = africastalking.Airtime

sb.set()
sb.set_style('darkgrid')
sb.set_palette('viridis')

pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 1000)

warnings.filterwarnings('ignore')


try:
    # check if the key exists in session state
    _ = st.session_state.keep_graphics
except AttributeError:
    # otherwise set it to false
    st.session_state.keep_graphics = False


with st.sidebar:
	selected = option_menu(
		menu_title = 'PesaWise',
		options = ['Assistant', 'Loans & Savings', 'Stocks', '🧭Trading Investments', '⚓Mortgages', '🚑Insurance',  '💱Crypto', '💲Taxes', '🤑Consultants', '🏛️Institutions', '📰Report Analysis', '♻️Subscribe'],
		icons = ['speedometer', 'graph-up-arrow', ':moneybag:', ':money_with_wings:'],
		menu_icon = 'cast',
		default_index = 0
		)
def load_lottiefile(filepath: str):
	with open(filepath, 'r') as file:
		return json.load(file)

fin_lottie = load_lottiefile('D:/Web_Development/Streamlit Deployment Projects/Dreamers Vault/animation/fin1.json')
fin2_lottie = load_lottiefile('D:/Web_Development/Streamlit Deployment Projects/Dreamers Vault/animation/fin2.json')
fin3_lottie = load_lottiefile('D:/Web_Development/Streamlit Deployment Projects/Dreamers Vault/animation/fin3.json')


if selected == 'Assistant':
	
	st.image('../source/img1.webp', width = 400)
	st.header('Welcome to PesaWise Virtual Assistant')
	st.subheader('Your financial advicer')
	st.markdown("""

	## Financial Literacy?
	
	Financial literacy is the ability to understand and effectively use various financial skills, including personal financial management, budgeting, and investing.

	When you are financially literate, you have the essential foundation for a smart relationship with money. This can help start a lifelong journey of learning about the financial aspects of your life. The earlier you start to become financially literate, 
	the better off you'll be because education is the key to a successful financial future.
	
	### Key Takeaways
	The term “financial literacy” refers to understanding a variety of important financial skills and concepts.
	Financially literate people are generally less vulnerable to financial fraud.
	A strong foundation of financial literacy can help support various life goals, such as saving for education or retirement, using debt responsibly, and running a business.
	Key aspects of financial literacy include knowing how to create a budget, plan for retirement, manage debt, and track personal spending.
	Financial literacy can be obtained through reading books, listening to podcasts, subscribing to financial content, or talking to a financial professional.



	### Why Financial Literacy Matters
	#### It Supports Financial Well-Being
	Day-to-day living expenses, living within your means, short-term borrowing, long-term budget forecasting. To manage these and other essential financial realities properly as you go through life, you must be financially literate.

	It is important to plan and save enough to provide adequate income in retirement while avoiding high levels of debt that might result in bankruptcy, defaults, and foreclosures.

	In its "Economic Well-Being of U.S. Households in 2022" report, the U.S. Federal Reserve System Board of Governors found that many Americans are not prepared for retirement. Twenty-eight percent indicated that they have no retirement savings, while about 31% of those not yet retired felt that their retirement savings were on track. Among those who have self-directed retirement savings, about 63% admitted to feeling low levels of confidence in making retirement decisions.
	3

	#### Millennials' Challenge
	Lack of financial literacy has left millennials—the largest share of the American workforce—unprepared for a severe financial crisis, according to research by the TIAA Institute. Even among those who reported having a high knowledge of personal finance, only 19% answered questions about fundamental financial concepts correctly.
	4

	Forty-three percent reported using expensive alternative financial services, such as payday loans and pawnshops. More than half lacked an emergency fund to cover three months’ of expenses, and 37% were financially fragile (defined as unable or unlikely to be able to come up with $2,000 within a month in the event of an emergency).
	4

	Millennials also carry large amounts of student loan and mortgage debt. In fact, 44% of them said they have too much debt.
	5

	Though these may seem like individual problems, they have a wider effect on the entire population than previously believed. The lack of knowledge of mortgage products prior to the 2008 financial crisis created widespread vulnerability to predatory lending. The financial impact of that crisis affected the entire economy.

	Financial literacy is an issue with broad implications for economic health.

	### Benefits of Financial Literacy
	Broadly speaking, the benefit of financial literacy is that it empowers individuals to make smarter decisions about their finances. In addition:

	Financial literacy can prevent devastating financial mistakes: Floating rate loans may have different interest rates each month, while traditional individual retirement account (IRA) contributions can’t be withdrawn until retirement. For someone unaware of these and other financial facts, seemingly innocent financial decisions may have long-term implications that cost them money or impact life plans. Financial literacy helps individuals avoid making mistakes with their personal finances.
	
	Financial literacy prepares people for financial emergencies: Topics such as saving or emergency preparedness get individuals ready for uncertain times. Though losing a job or having a major unexpected expense can be financially impactful, an individual can cushion the blow by saving regularly.
	
	Financial literacy can help individuals reach their goals: By better understanding how to budget and save money, individuals can create plans that define expectations, hold them accountable to their finances, and set a course for achieving important financial goals. Though someone may not be able to afford a dream today, they can create a plan that can help make it happen.
	
	Financial literacy gives rise to confidence: Imagine having to make a life-changing financial decision without all the necessary information. With knowledge about finances, individuals can approach major life choices with greater confidence. They'll be more likely to achieve the outcome they desire and less likely to be surprised or negatively impacted by unforeseen outcomes.
	
	### Strategies to Improve Financial Literacy Skills
	Developing financial literacy involves learning and practicing skills related to budgeting, managing, and paying off debts, and more. It means understanding and using credit and investment products wisely. The good news is that, no matter where you are in life and financially, it’s never too late to start practicing good financial habits.

	Here are several practical strategies to consider.

	#### 1.Create a Budget
	Track how much money you receive each month and how much you spend. You can use an Excel spreadsheet, paper, or a budgeting app. Your budget should include income (paychecks, investments, alimony), fixed expenses (rent/mortgage payments, utilities, loan payments), discretionary spending (nonessentials such as eating out, shopping, and travel), and savings. Pairing your budget with an expense tracking app can help identify where you are spending each month and where you might be able to save.

	#### 2.Pay Yourself First
	To build savings, this reverse budgeting strategy involves choosing a savings goal, such as paying for higher education, deciding how much you want to contribute toward it each month, and setting that amount aside before you divvy up the rest of your expenses.

	#### 3.Pay Bills Promptly
	Stay on top of monthly bills, making sure that your payments are always sent to arrive on time. Consider taking advantage of automatic debits from a checking account or bill-pay apps, and sign up for payment reminders (by email, phone, or text).

	#### 4.Get Your Credit Report
	Once a year, consumers can request a free credit report from each of the three major credit bureaus—Equifax, Experian, and TransUnion—through the federally created website AnnualCreditReport.com.
	6

	Review these reports and dispute any errors by informing the credit bureau of inaccuracies. Because you can get three of them, consider spacing out your requests throughout the year to monitor your credit regularly.

	In a 2022 survey by the Federal Reserve, 27% of adults in the U.S. reported not "doing okay" financially. The number who reported not living comfortably increased from 2021.
	7
	#### 5.Check Your Credit Score
	A good credit score enables you to obtain the best interest rates on loans and credit cards, among other benefits. Monitor your score via a free credit monitoring service. Or, if you can afford to and want to add an extra layer of protection for your personal information, use a credit monitoring service. In addition, be aware of what can raise or lower your scores, such as credit inquiries and credit utilization ratios.

	#### 6.Manage Debt
	Use your budget to stay on top of debt by reducing spending and increasing repayment. Develop a debt reduction plan, such as paying down the loan with the highest interest rate first. If your debt is excessive, contact lenders to renegotiate repayment, consolidate loans, or find a debt counseling program.

	#### 7.Invest in Your Future
	If your employer offers a 401(k) retirement savings account, be sure to sign up and contribute the maximum to receive the employer match. Consider opening an IRA and creating a diversified investment portfolio of stocks, fixed income, and commodities. If necessary, seek financial advice from professional advisors to help you determine how much money you will need to retire comfortably and develop strategies to reach your goal.

	### 
	Using [Openai platform](https://platform.openai.com/account/api-keys) chatgpt-3 to generate api and pull Get request from their servers.
	""")

	

	###############################################################################


	tab1, tab2 = st.tabs(["☎ Voice Command", "📳 Messaging "])
	# data = np.random.randn(10, 1)

	# tab1.subheader("A tab with a chart")
	# tab1.line_chart(data)

	with tab1:
		import streamlit as st
		import pyttsx3
		import tempfile
		import os

		# Initialize the pyttsx3 engine
		engine = pyttsx3.init()

		# Function to save the spoken text to a temporary audio file
		def text_to_speech(text):
		    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
		        tmp_filename = tmp_file.name
		    engine.save_to_file(text, tmp_filename)
		    engine.runAndWait()
		    return tmp_filename

		# Streamlit app
		st.title("Financial Literacy Assistant")

		# Example scenarios and responses
		
		scenarios = {
		    "budgeting": "If you want to manage your finances better:\n"
		                 "- Create a budget that outlines your income and expenses.\n"
		                 "- Track your spending to identify areas where you can save money.\n"
		                 "- Set financial goals and allocate funds towards them each month.\n"
		                 "- Use budgeting tools or apps to simplify the process.\n"
		                 "- Regularly review and adjust your budget as your circumstances change.",

		    "saving": "If you want to grow your savings:\n"
		              "- Set a savings goal and make it specific, measurable, and time-bound.\n"
		              "- Open a dedicated savings account to avoid dipping into your funds.\n"
		              "- Automate your savings by setting up direct transfers from your paycheck.\n"
		              "- Cut unnecessary expenses to increase the amount you can save.\n"
		              "- Take advantage of high-interest savings accounts or investment opportunities.",

		    "investing": "If you want to start investing:\n"
		                 "- Educate yourself about different investment options like stocks, bonds, and mutual funds.\n"
		                 "- Assess your risk tolerance and choose investments that align with it.\n"
		                 "- Diversify your portfolio to reduce risk.\n"
		                 "- Start small and gradually increase your investments as you gain confidence.\n"
		                 "- Consult a financial advisor for professional guidance if needed.",

		    "debt management": "If you want to manage your debts effectively:\n"
		                       "- List all your debts, including amounts, interest rates, and due dates.\n"
		                       "- Prioritize paying off high-interest debts first to save money over time.\n"
		                       "- Consider consolidating your debts to simplify payments and lower interest rates.\n"
		                       "- Avoid taking on new debt unless absolutely necessary.\n"
		                       "- Reach out to creditors to negotiate repayment terms if you're struggling.",

		    "retirement planning": "If you want to prepare for retirement:\n"
		                           "- Start saving early to take advantage of compound interest.\n"
		                           "- Contribute to retirement accounts like a 401(k) or IRA.\n"
		                           "- Calculate how much you'll need based on your desired lifestyle in retirement.\n"
		                           "- Regularly review and adjust your retirement plan as your goals change.\n"
		                           "- Seek advice from a financial planner to ensure you're on track.",

		    "credit management": "If you want to maintain a good credit score:\n"
		                         "- Pay your bills on time and in full to avoid late fees and penalties.\n"
		                         "- Keep your credit utilization ratio below 30%.\n"
		                         "- Check your credit report regularly for errors or signs of fraud.\n"
		                         "- Avoid opening too many new credit accounts in a short period.\n"
		                         "- Use your credit responsibly and only borrow what you can repay.",

		    "emergency fund": "If you want to create an emergency fund:\n"
		                      "- Aim to save 3-6 months' worth of living expenses.\n"
		                      "- Keep the funds in a separate, easily accessible savings account.\n"
		                      "- Contribute to your emergency fund regularly, even if it's a small amount.\n"
		                      "- Avoid using the fund for non-emergencies.\n"
		                      "- Replenish the fund immediately after using it for emergencies.",

		    "financial education": "If you want to improve your financial knowledge:\n"
		                           "- Read books, articles, and blogs about personal finance and investing.\n"
		                           "- Take online courses or attend workshops on financial literacy.\n"
		                           "- Follow reputable financial advisors and educators on social media.\n"
		                           "- Stay updated on economic trends and how they might affect your finances.\n"
		                           "- Practice what you learn by applying it to your financial planning.",

		    "tax planning": "If you want to optimize your taxes:\n"
		                    "- Keep detailed records of your income, expenses, and deductions.\n"
		                    "- Take advantage of tax credits and deductions for which you're eligible.\n"
		                    "- Consider contributing to tax-advantaged accounts like HSAs or 401(k)s.\n"
		                    "- File your taxes on time to avoid penalties.\n"
		                    "- Consult a tax professional for complex tax situations or advice.",

		    "wealth building": "If you want to build wealth:\n"
		                        "- Focus on increasing your income through career advancement or side hustles.\n"
		                        "- Control your spending to maximize savings and investments.\n"
		                        "- Invest in assets that grow in value over time, like real estate or stocks.\n"
		                        "- Protect your wealth with insurance and a solid financial plan.\n"
		                        "- Be patient and disciplined, as wealth building takes time.",

		    "insurance": "If you want to protect your assets and income:\n"
		                 "- Understand the different types of insurance, like health, life, auto, and home.\n"
		                 "- Assess your risks and choose policies that provide adequate coverage.\n"
		                 "- Compare quotes from multiple insurers to get the best rates.\n"
		                 "- Review your policies regularly to ensure they meet your changing needs.\n"
		                 "- File claims promptly and accurately in case of loss or damage.",

		    "entrepreneurship": "If you want to start a business:\n"
		                        "- Develop a business plan outlining your goals, target market, and financial projections.\n"
		                        "- Save or secure funding to cover startup costs and initial operations.\n"
		                        "- Keep personal and business finances separate with a dedicated business account.\n"
		                        "- Track your income and expenses to ensure profitability.\n"
		                        "- Learn about tax obligations and compliance for businesses in your area."
		}




		# Prompt user for a disaster scenario
		scenes = [i for i in scenarios.keys()]
		user_input = st.selectbox("Select category (Budget, investments, entrepreneurship, insurance):", scenes).lower()

		# Generate and display response if input matches a scenario
		if user_input in scenarios:
		    response = scenarios[user_input]
		    st.write(response)
		    
		    # Convert text to speech and save it to a temporary audio file
		    audio_filename = text_to_speech(response)
		    
		    # Play the audio file
		    audio_file = open(audio_filename, 'rb')
		    audio_bytes = audio_file.read()
		    st.audio(audio_bytes, format='audio/mp3')
		    
		    # Clean up the temporary audio file
		    os.remove(audio_filename)
		else:
		    if user_input:
		        st.audio("I'm sorry, I do not have information on that financial data.")



	################################################################################


	# User input form
	query = st.text_input("Enter your financial question:")
	button_clicked = st.button("Submit")

	# Function to query OpenAI for financial advice
	def get_financial_advice(question):
	    try:
	        response = openai.ChatCompletion.create(
	            model="gpt-4",
	            messages=[
	                {"role": "system", "content": "You are a financial expert."},
	                {"role": "user", "content": question},
	            ],
	            stream=True  # Streaming responses
	        )
	        advice = ""
	        for chunk in response:
	            advice += chunk["choices"][0]["delta"].get("content", "")
	            st.text(advice)  # Stream output
	        return advice
	    except Exception as e:
	        st.error(f"Error querying OpenAI: {e}")
	        return None

	# Function to find financial institutions in Kenya
	def find_financial_institutions():
	    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
	    params = {
	        "query": "financial institutions in Kenya",
	        "key": google_maps_api_key,
	    }
	    try:
	        response = requests.get(url, params=params)
	        data = response.json()
	        institutions = []
	        for place in data.get("results", []):
	            name = place.get("name")
	            address = place.get("formatted_address")
	            link = f"https://www.google.com/maps/place/?q=place_id:{place.get('place_id')}"
	            institutions.append({"name": name, "address": address, "link": link})
	        return institutions
	    except Exception as e:
	        st.error(f"Error querying Google Maps: {e}")
	        return []

	# Handle user query
	if button_clicked and query:
	    st.write("### Chatbot's Response:")
	    if "locate" in query.lower() or "financial institution" in query.lower():
	        st.write("Locating financial institutions in Kenya...")
	        institutions = find_financial_institutions()
	        if institutions:
	            for i, inst in enumerate(institutions, start=1):
	                st.write(f"**{i}. {inst['name']}**")
	                st.write(f"Address: {inst['address']}")
	                st.write(f"[View on Google Maps]({inst['link']})")
	        else:
	            st.write("No institutions found. Please try again.")
	    else:
	        st.write("Fetching financial advice...")
	        get_financial_advice(query)






	##################################################################################

	



if selected == 'Loans & Savings':
	st.write('''
		# Finance
		Finance is the study and discipline of [money](https://en.wikipedia.org/wiki/Money), [currency](https://en.wikipedia.org/wiki/Currency) and [capital assets](https://en.wikipedia.org/wiki/Capital_asset). 
		It is related to, but not synonymous with [economics](https://en.wikipedia.org/wiki/Economics), which is the study of production, distribution, and consumption of money, assets, goods and services (the discipline of financial economics bridges the two). 
		Finance activities take place in financial systems at various scopes, thus the field can be roughly divided into [personal, corporate, and public finance].

		''')
	col1, col2 = st.columns(2)
	with col1:
		st_lottie(fin_lottie,
			speed=1,
			reverse=False,
			loop=True,
			quality="high",
			width=300,
			height=250,
			)
		st.write('''

			### Areas of Finance
			- **Personal Finance** -
			the mindful planning of monetary spending and saving, while also considering the possibility of future risk". Personal finance may involve paying for education, 
			financing durable goods such as real estate and cars, buying insurance, investing, and saving for retirement.

			- **Corporate Finance** -
			deals with the actions that managers take to increase the value of the firm to the shareholders, the sources of funding and the capital structure of corporations, 
			and the tools and analysis used to allocate financial resources.

			- **Public Finance** -
			describes finance as related to sovereign states, sub-national entities, and related public entities or agencies. It generally encompasses a long-term strategic 
			perspective regarding investment decisions that affect public entities.

			- **Quantitative Finance** -
			also referred to as "mathematical finance" – includes those finance activities where a sophisticated mathematical model is required.
			[read more](https://corporatefinanceinstitute.com/resources/data-science/quantitative-finance/#:~:text=Quantitative%20finance%20is%20the%20use,relates%20to%20portfolio%20management%20applications.)
			
			''')
	with col2:
		st.write('''

			### Financial system

			As above, the financial system consists of the flows of capital that take place between individuals and households [(personal finance)](https://en.wikipedia.org/wiki/Personal_finance), 
			governments [(public finance)](https://en.wikipedia.org/wiki/Public_finance), and businesses [(corporate finance)](https://en.wikipedia.org/wiki/Corporate_finance). "Finance" thus studies the process of channeling money from savers and 
			investors to entities that need it. [b] Savers and investors have money available which could earn interest or dividends if put to productive use. 
			Individuals, companies and governments must obtain money from some external source, such as loans or credit, when they lack sufficient funds to operate.
			
			''')
		st_lottie(fin2_lottie,
			speed=1,
			reverse=False,
			loop=True,
			quality="high",
			width=300,
			height=250,
			)
		st_lottie(fin3_lottie,
			speed=1,
			reverse=False,
			loop=True,
			quality="high",
			width=300,
			height=250,
			)
		st.write('**Money-festing** :smiley:')
	st.image('D:/Web_Development/Streamlit Deployment Projects/Dreamers Vault/source/Interest Payout.png')
	st.write('''
			### Loan Calculator

			This is app is going to determine how long it takes to repay a loan borrowed, given amount borrowed, interest rates and payment terms 
		''')
	
	
	with st.form(key='form1'):
		col1, col2, col3 = st.columns(3)
		with col1:
			loan_amount = st.number_input('amount borrowed', value=0, min_value=0, max_value=int(10e10))

		with col2:
			payment_rate = st.slider('Interest rate', 0.0, 10.0)/100.0

		with col3:
			monthly_amount = st.number_input('Monthly re-payment', min_value=0, max_value=int(10e10))

		# submit_label = f'<i class="fas fa-calculator">Calculate</i> '
		# submit = st.form_submit_button(submit_label)

		submit = st.form_submit_button(label='Calculate')

		#Determine the total period it takes to repay off a loan
		# bal = 5000
		# interestRate = 0.13
		# monthlyPayment = 500

	if submit not in st.session_state:
		df = pd.DataFrame(columns=['End Month', 'Loan Amount', 'Interest Charge'])
		
		current_date = datetime.today()
		# print(current_date)

		end_month_day = calendar.monthrange(current_date.year, current_date.month)[1]
		days_left = end_month_day - current_date.day

		next_month_start_date = current_date + timedelta(days=days_left + 1)
		end_month = next_month_start_date

		period_count = 0
		total_int = 0
		data = []

		while loan_amount > 0:
		    int_charge = (payment_rate / 12) * loan_amount
		    loan_amount += int_charge
		    loan_amount -= monthly_amount

		    if loan_amount <= 0:
		        loan_amount = 0
		    total_int += int_charge
		    print(end_month, round(loan_amount, 2), round(int_charge, 2))

		    period_count += 1
		    new_date = calendar.monthrange(end_month.year, end_month.month)[1]
		    end_month += timedelta(days=new_date)

		    # df = df.append({'End Month': end_month, 'Loan Amount': round(loan_amount, 2), 'Interest Charge': round(int_charge, 2)}, ignore_index=True)

		    data.append([end_month.date(), round(loan_amount, 2), round(int_charge, 2)])

		    if loan_amount == 0:
		        break

		print('Total Interest Rate paid: ', total_int)
		df = pd.DataFrame(data, columns=['next_pay_date', 'amount_remaining', 'interest_amount'])

		
		years = int(period_count // 12)
		months_remaining = round(period_count % 12)
		print(f"{years} years and {months_remaining} months")

		col1, col2 = st.columns(2)
		with col1:
			st.dataframe(df, use_container_width=True)

		with col2:
			st.write('Loan payment due')
			col1, col2, col3 = st.columns(3)
			col1.metric("", str(years), " yrs")
			col2.metric("", str(months_remaining), " months")
			st.metric("Total Interest Paid", "sh. " + str(round(total_int)), "")
			# col2.metric("Wind", "9 mph", "-8%")
			# col3.metric("Humidity", "86%", "4%")

	with st.popover("Download Report"):

		with st.form(key="report"):
			phone_number = st.number_input('Phone Number', value=0, min_value=0, max_value=int(10e10))

			submit_report = st.form_submit_button("Send")

			def send_report():
				amount = "10"
				currency_code = "KES"


				recipients = [f"+254{str(phone_number)}"]
				airtime_rec = "+254" + str(phone_number)
				print(recipients)
				# print(phone_number)

				# Set your message
				message = f"Welcome to PesaWise \n Your account was succesful created";
				# Set your shortCode or senderId
				sender = "AFTKNG"
				try:
					responses = airtime.send(phone_number=airtime_rec, amount=amount, currency_code=currency_code)
					response = sms.send(message, recipients, sender)
					
					print(response)
					print(responses)
				except Exception as e:
					print(f'Houston, we have a problem: {e}')

		if submit_report not in st.session_state:
			send_report()

		
		else:
			pass

			# send_report()







# --------------------------------------End Finance Section ----------------------------------------------------- #



if selected == 'Stocks':

	header = st.container()
	local_data = st.container()

	with header:
		st.image('../source/img7.jpg')
		st.title('GLOBAL STOCKS MARKET DATA')
		st.write('**What do stocks mean?**')
		st.write('A stock represents a share in the ownership of a company, including a claim on the companys earnings and assets. As such, stockholders are partial owners of the company. When the value of the business rises or falls, so does the value of the stock.')


	with local_data:
		col1, col2 = st.columns(2)
		
		with col1:
			st.image('../source/img6.png', width=350)

		with col2:
			st.image('../source/img4.webp', width=350)

		
		st.write("<h3 style='text-align: center; color: white;'>One place for your portfolios, <br>metrics and more<h3>", unsafe_allow_html=True)
		st.write('Gain insights, see trends and get real-time updates from well researched and analyzed datasets.')
		st.write('However the developer will integrate the results with Machine Learning algorithms for effecient and predictive output. This will boost accuracy and confidence in investing in stocks.')
		st.write('sorry I wasnt listening.....I was thinking about TRADING')


		df = pd.read_csv('../source/big_tech_stock_prices.csv')
		st.dataframe(df.head())

		# Data Cleaning
		df['date'] = pd.to_datetime(df['date'])

		st.write('### Statistical Representation of Data')

		col1, col2 = st.columns(2)
		
		with col1:
			st.write('Rows ', df.shape[0], 'Columns / Series ', df.shape[1])
			# st.write('Columns / Series ', df.shape[1])
		
			# Capture the output of df.info()
			buffer = io.StringIO()
			df.info(buf=buffer)
			info_str = buffer.getvalue()

			# Display df.info() output in Streamlit
			st.write('Summary of the dataframe')
			st.text(info_str)

		with col2:
			st.write('')
			st.write('')
			st.write('')
			st.write('')
			st.write('Description of the dataframe')
			st.dataframe(df.describe())

		st.write('### Graphical Presentation of Data')

		def get_numerical(df):
			numerical_list = []
			categories = df.select_dtypes(include=['float64', 'int64'])
			for i in categories:
				numerical_list.append(i)
			print(numerical_list)
			return numerical_list

		plot_hist_column = st.selectbox('Select dataframe series', (i for i in get_numerical(df)))

		print(plot_hist_column)

		fig = px.histogram(df[plot_hist_column], 
				title = 'Stock Distribution Plot for ' +  str(plot_hist_column) + ' series'
			)
		
		print(df[plot_hist_column])
		st.plotly_chart(fig)
		
		def get_categories(df):
		    cat = []
		    categories = df.select_dtypes(include=['float64', 'int64'])
		    for i in categories:
		        cat.append(i)
		    print(cat)
		    # fig = sb.heatmap(df[cat].corr(), annot=True, linewidths=0.5)
		    fig = px.imshow(df[cat].corr(), text_auto=True, aspect='auto', 
		    	title = 'Pearsons Correlation of Columns'
		    	)
		    st.plotly_chart(fig)

		get_categories(df)

		col1, col2 = st.columns(2)

		with col1:
			stock_company = st.selectbox('Select Symbol company', df['stock_symbol'].unique())

		with col2:
			stock_clause = st.selectbox('Select Stock Clause', get_numerical(df))

		company_group = df.groupby('stock_symbol').get_group(stock_company)
		
		
		pivot_df = company_group.pivot(index='stock_symbol', columns='date', values=stock_clause)
		print(pivot_df)

		fig = go.Figure(data=go.Heatmap(
			z=pivot_df,
	        x=company_group['date'],
	        y=company_group[stock_clause],
	        colorscale='Viridis'))
		
		fig.update_layout(
			title=f"Daily stocks charts from  {df['date'].dt.date.min()} to {df['date'].dt.date.max()}",
			# xaxis_title='Date',
			yaxis_title=f'{stock_clause} Price',
			legend_title='Company'
			)
		st.plotly_chart(fig)
		

		
		stock_symbol = df.groupby('stock_symbol').get_group(stock_company)

		
		fig = go.Figure()

		# Adding a trace for the company's open stock prices
		fig.add_trace(go.Scatter(x=stock_symbol['date'], y=stock_symbol['open'], mode='lines'))

		# frames = [go.Frame(data=[go.Scatter(x=company_group['date'][:k+1], y=company_group['open'][:k+1])],
	    #                name=str(company_group['date'].iloc[k])) for k in range(len(company_group.head(50)))]

		# fig.frames = frames

		# Setting the title and labels
		fig.update_layout(
			title=f'Open Stocks of the Tech company {stock_company}',
			xaxis_title='Date',
			yaxis_title='Open Price',
			legend_title='Company'
			)



		# Display the figure
		st.plotly_chart(fig)


		def load_lottiefile(filepath: str):
			with open(filepath, 'r') as file:
				return json.load(file)
		
		animation_1 = load_lottiefile('../source/stocks1.json')

		st_lottie(animation_1,
				speed=1,
				reverse=False,
				loop=True,
				quality="high",
				width=500,
				height=450,
				)
		
		# finance_lottie = load_lottieurl("https://app.lottiefiles.com/share/9e58a2cc-e627-4b6a-a0b4-3fa95571236c")


#############################################################################################################################

if selected == 'Trading Investments':

# 	st.video('../source/stock_animation.mp4', format='mp4')

# 	import yfinance as yf

# 	tickers = yf.Tickers('msft aapl goog tsla scom coop kcb eqt kq nse bat bamb totl nmg nbk dtk')

# 	# access each ticker 
# 	stock = tickers.tickers[str('nmg').upper()].history(period="max")

# 	df2 = pd.DataFrame(stock).head(1000)

# 	if {'Dividends', 'Stock Splits'}.issubset(df2.columns):
# 		df2.drop(columns=['Dividends', 'Stock Splits'], inplace=True)
	

# 	st.dataframe(df2)
# 	st.write(df2.shape)
# 	st.write(df2.columns)
# 	df2.reset_index(inplace=True)

# 	buffer = io.StringIO()
# 	df2.info(buf=buffer)
# 	info_str = buffer.getvalue()

# 	# Display df.info() output in Streamlit
# 	st.write('Summary of the dataframe')
# 	st.text(info_str)



# 	fig = go.Figure()

# 	fig.add_trace(go.Scatter(x=df2.index, y = df2['High'], mode='lines'))



# 	# Add frames for animation
# 	frames = [go.Frame(data=[go.Scatter(x=df2['Date'][:k+1], y=df2['High'][:k+1])],
# 	                   name=str(df2['Date'].iloc[k])) for k in range(len(df2))]

# 	fig.frames = frames

# 	# Update layout with animation settings
# 	fig.update_layout(
# 	    title=f'High Stocks of the Tech company',
# 	    xaxis_title='Date',
# 	    yaxis_title='High Price',
# 	    legend_title='Company'
# 	    # updatemenus=[dict(type='buttons', showactive=False,
# 	    #                   buttons=[dict(label='Play',
# 	    #                                 method='animate',
# 	    #                                 args=[None, dict(frame=dict(duration=50, redraw=True), fromcurrent=True)])])],
# 	    # # Automatically start the animation
# 	    # transition={'duration': 100},
# 	    # # frame={'duration': 100, 'redraw': True},
# 	    # sliders=[dict(steps=[dict(method='animate', args=[[f.name], dict(mode='immediate', frame=dict(duration=50, redraw=True), transition=dict(duration=0))], label=f.name) for f in frames])]
# 	)


# 	st.plotly_chart(fig)


	
##########################################################################################
	

	# Streamlit app
	st.title('Market Security Stocks')

	# User selects a stock symbol
	# stock_symbol = st.selectbox('Select Symbol company', ['AAPL', 'GOOG', 'MSFT'])

	
	with st.form(key="input_parameters"):

		tk = yf.Tickers('msft aapl goog tsla scom coop kcb eqt kq nse bat bamb totl nmg nbk dtk')



		symbol = []
		for i in tk.symbols:
			symbol.append(i)
			symbol.sort(reverse=False)


		ticker = st.selectbox('select ticker symbol', symbol)

		submitted = st.form_submit_button('explore')


		# Fetch the real-time data
		stock = tk.tickers[str(ticker).upper()].history(period="max")

		data = pd.DataFrame(stock)#.head(1000)

		st.write(data.index.max())


		if {'Dividends', 'Stock Splits'}.issubset(data.columns):
			data.drop(columns=['Dividends', 'Stock Splits'], inplace=True)

		today_high = round(data["High"].iloc[0] - data["High"].iloc[1], 2)
		today_open = round(data["Open"].iloc[0] - data["Open"].iloc[1], 2)
		today_high = round(data["High"].iloc[0] - data["High"].iloc[1], 2)

		st.write(f'Market summary > {ticker}')

		trade_col1, trade_col2, trade_col3, trade_col4 = st.columns(4)

		with trade_col1:
			st.metric(label='Net Gain/Loss', value=str(round(data["High"].iloc[0], 2)), delta=str(today_high) + " Today")

		with trade_col2:
			st.metric(label='Open', value=str(round(data["Open"].iloc[0], 2)), delta=str(today_open))

		with trade_col3:
			st.metric(label='Date', value=str(datetime.today().year), delta=str(datetime.today().strftime('%A')))
			# st.write(str(datetime.today().date()))

	
		data.reset_index(inplace=True)

		# Placeholder for the plot
		placeholder = st.empty()


	if submitted or st.session_state.keep_graphics:

		future_prediction(data)
		regression_model(data)

		# Infinite loop to update the plot with real-time data
		while True:
		    # Create the plot
		    fig1 = go.Figure()
		    
		    fig1.add_trace(go.Scatter(x=data['ds'], y=data['y'], mode='lines'))
		    
		    # Update layout
		    fig1.update_layout(
		        title=f'{ticker.upper()}',
		        xaxis_title='Time',
		        yaxis_title='Price',
		        legend_title='Stock Symbol'
		    )
		    
		    # Update the plot in the placeholder
		    placeholder.plotly_chart(fig1, use_container_width=True, key="iris")
		    
		    # Wait for a few seconds before updating
		    time.sleep(5)  # Adjust the sleep time as needed

		st.plotly_chart(placeholder)

	
	




if selected ==  'Model':
	pass
	# regression_model(data)
	# subprocess.run([f"{sys.executable}", "../model/regression.py"])
	# st.plotly_chart(fig)


if selected == '🏛️Institutions':
	import folium as fl
	# m = fl.Map(location=[1.286389, 36.817223], zoom_start=7)

	# st_map = st_folium(m, width=700, height=450)

	# st.markdown("![Foo](https://www.google.com/maps/search/financial+institutions,+banks,+saccos/@-1.2996977,36.7871538,15z?entry=ttu&g_ep=EgoyMDI0MTIwMi4wIKXMDSoASAFQAw%3D%3D)(http://google.com.au/)")

	import streamlit as st
	import folium as fl
	from streamlit_folium import st_folium
	import requests

	# Function to fetch financial institutions using Overpass API
	def fetch_osm_data(query, bounding_box):
	    url = "https://overpass-api.de/api/interpreter"
	    osm_query = f"""
	    [out:json];
	    node["amenity"="{query}"]({bounding_box});
	    out;
	    """
	    response = requests.get(url, params={"data": osm_query})
	    if response.status_code == 200:
	        return response.json()["elements"]
	    else:
	        st.error("Error fetching data from OpenStreetMap API.")
	        return []

	# Streamlit App
	st.title("Financial Institutions, Banks, Saccos and ATMs near me..")

	# Define bounding box for Nairobi (latitude_min, longitude_min, latitude_max, longitude_max)
	nairobi_bbox = "-1.406108,36.641423,-1.145753,37.010971"

	# Fetch data for banks and ATMs
	st.write("Fetching financial institutions in Nairobi...")
	banks_data = fetch_osm_data("bank", nairobi_bbox)
	fintechs_data = fetch_osm_data("financial institutions", nairobi_bbox)
	saccos_data = fetch_osm_data("saccos", nairobi_bbox)
	atms_data = fetch_osm_data("atm", nairobi_bbox)

	# Initialize Folium Map
	m = fl.Map(location=[-1.286389, 36.817223], zoom_start=13)

	# Add markers for banks and ATMs
	for bank in banks_data:
	    fl.Marker(
	        location=[bank["lat"], bank["lon"]],
	        popup=bank.get("tags", {}).get("name", "Unnamed Bank"),
	        tooltip="Bank",
	        icon=fl.Icon(color="blue", icon="info-sign"),
	    ).add_to(m)

	for fins in fintechs_data:
	    fl.Marker(
	        location=[fintechs["lat"], fintechs["lon"]],
	        popup=fintechs.get("tags", {}).get("name", "Unnamed Fintech"),
	        tooltip="Fintechs",
	        icon=fl.Icon(color="red", icon="info-sign"),
	    ).add_to(m)

	for atm in atms_data:
	    fl.Marker(
	        location=[atm["lat"], atm["lon"]],
	        popup=atm.get("tags", {}).get("name", "Unnamed ATM"),
	        tooltip="ATM",
	        icon=fl.Icon(color="green", icon="info-sign"),
	    ).add_to(m)

	# Display the map
	st_map = st_folium(m, width=700, height=500)


	# st.write("### Financial Institutions Table")

	# for bank in banks_data:
	#     name = bank.get("tags", {}).get("name", "Unnamed Bank")
	#     banks_data.append({"Type": "Bank", "Name": name})
	# # st.dataframe(bank_data)

	# for atm in atms_data:
	#     name = atm.get("tags", {}).get("name", "Unnamed ATM")
	#     atms_data.append({"Type": "ATM", "Name": name})
	# # st.dataframe(atm_data)

	# # Combine results into a single DataFrame
	# all_data = pd.DataFrame(banks_data + atms_data).head(20)


if selected == "🧭Trading Investments":
	with st.form(key = 'user_submit'):
		ai_bot = st.write('PesaWise: How may I help you', '''
			''')

		human = st.text_area('Human: ', '''
			''')

		submit = st.form_submit_button(label = 'submit')

	audio = pt.init()
	audio.say(ai_bot)

	# openai.api_key = "AIzaSyCQhclyS920GA_IRnJ1Uq_u3cp5r0CgvTk"

	start_sequence = ai_bot
	restart_sequence = human


	response = openai.Completion.create(
	  model="o1-preview-2024-09-12",
	  prompt=str(human),
	  temperature=0.9,
	  max_tokens=150,
	  top_p=1,
	  frequency_penalty=0,
	  presence_penalty=0.6,
	  stop=[" Human:", " AI:"]
	)

	print(completion.choices[0].message)


	if submit==True:
	    ai_bot_resp = st.write(response.choices[0].text)
	else:
	    st.write('How may I help you freind')

	while True:
		audio = pt.init()
		audio.say('Here is the answer to your question')
		audio.say(response.choices[0].text)
		audio.runAndWait()
			