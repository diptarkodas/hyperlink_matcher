import requests
from bs4 import BeautifulSoup

# Function to read keywords from a file
def read_keywords(file_path):
    with open(file_path, 'r') as file:
        keywords = [line.strip() for line in file]
    return keywords

def fetch_hyperlinks_and_descriptions(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        hyperlinks = []
        descriptions = []
        
        # Find all the <dt> tags containing hyperlinks
        dt_tags = soup.find_all('dt')
        for dt in dt_tags:
            # Find the PDF link within the <dt> tag
            pdf_link = dt.find('a', href=True, string='pdf')
            if pdf_link:
                href = "https://arxiv.org" + pdf_link['href']
                hyperlinks.append(href)
                
                # Find the corresponding <dd> tag
                dd_tag = dt.find_next_sibling('dd')
                if dd_tag:
                    # Extract the title from the <div class='list-title'> tag
                    title_div = dd_tag.find('div', class_='list-title')
                    if title_div:
                        title = title_div.get_text(strip=True)
                    else:
                        title = ''
                    
                    # Extract the text from the <p class='mathjax'> tag
                    mathjax_tag = dd_tag.find('p', class_='mathjax')
                    if mathjax_tag:
                        mathjax_text = mathjax_tag.get_text(strip=True)
                    else:
                        mathjax_text = ''
                    
                    # Combine the title and mathjax text for description
                    description = title + '%%' + mathjax_text
                    descriptions.append(description)
                else:
                    descriptions.append('')
        
        return hyperlinks, descriptions
    except:
        return [], []

# Function to calculate the weight based on keyword matches
def calculate_weight(text, keywords):
    weight = 0
    for keyword in keywords:
        if keyword.lower() in text.lower():
            weight += 1
    return weight

# Read keywords from the keyword.dat file
keyword_file = 'keyword.dat'
keywords = read_keywords(keyword_file)


# Specify the website URLs to process
urls = [ 'https://arxiv.org/list/hep-ph/new',
         'https://arxiv.org/list/hep-th/new',
         'https://arxiv.org/list/cond-mat/new'

]

final = []

for website_url in urls :

# Fetch hyperlinks and their descriptions from the website
    hyperlinks, descriptions = fetch_hyperlinks_and_descriptions(website_url)
# Process each hyperlink and description pair and store them in a list
    results = []
    for hyperlink, description in zip(hyperlinks, descriptions):
        weight = calculate_weight(description, keywords)
        if weight > 0:
            results.append((hyperlink, description, weight))
    final.extend(results)

# Sort the results based on weights in descending order
final.sort(key=lambda x: x[2], reverse=True)
# Print the sorted list
print("Sorted List:")
for hyperlink, description, weight in final:
    title = description.split('%%', 1)[0]  # Extract the title from the description
    print("Hyperlink:", hyperlink)
    print("", title)
    print("Weight:", weight)
    print("---")


##if you want to send email to yourself just add in these lines 
##[ i am using outlook hence used smtp server as smtp.office365.com, different email clients have different ones ] : 


    
## Generate the consolidated list

# consolidated_list = "Consolidated List:\n\n"
# for hyperlink, description, weight in final:
#     title = description.split('%%', 1)[0]  # Extract the title from the description
#     consolidated_list += f"Hyperlink: {hyperlink}\n"
#     consolidated_list += f"Title: {title}\n"
#     consolidated_list += f"Weight: {weight}\n"
#     consolidated_list += "---\n"


# ##Send email with the consolidated list

# sender_email = "sending-email"
# sender_password = "sending-email-password"
# recipient_email = "your-receiving-email-here"

# today = date.today().strftime("%Y-%m-%d")

# message = MIMEMultipart()
# message["From"] = sender_email
# message["To"] = recipient_email
# message["Subject"] = f"papers for - {today}"

# message.attach(MIMEText(consolidated_list, "plain"))

# with smtplib.SMTP("smtp.office365.com", 587) as server:
#     server.starttls()
#     server.login(sender_email, sender_password)
#     server.send_message(message)

# print("Email sent successfully!")