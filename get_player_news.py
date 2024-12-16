import requests
from bs4 import BeautifulSoup

# TODO fix issues with punctuation in names
# format the link to be used to retreive news about the player
def format_player_url(player_name):
        """Format the player's name to match the URL structure."""
        formatted_name = player_name.lower().replace(" ", "-")
        return f"https://www.fantasypros.com/nfl/players/{formatted_name}.php"

# get the recent news from fantasypros using the player name
def get_player_news(player_name):

    player_url = format_player_url(player_name)
    response = requests.get(player_url)

    if response.status_code != 200:
        return f"Failed to retrieve data for {player_name}."

    soup = BeautifulSoup(response.text, "html.parser")
    # need div with infromation about the players, news, professional option, etc...
    player_news_section = soup.find("div", class_="subsection feature-stretch")
    

    if player_news_section:
        # need divs with class content that has news
        content_div = player_news_section.find("div", class_="content")
        if content_div:
            formatted_output = ""
           
            for news_block in content_div.find_all("a", href=True):
                news_title = news_block.text.strip()
                summary_tag = news_block.find_next_sibling("p")
                summary = summary_tag.text.strip() if summary_tag else "No summary available."

                # need to finf  "Fantasy Impact", then take the <p> values
                fantasy_impact_tag = summary_tag.find_next_sibling("p") if summary_tag else None
                if fantasy_impact_tag and "Fantasy Impact" in fantasy_impact_tag.text:
                    fantasy_impact = fantasy_impact_tag.find_next_sibling("p")
                    fantasy_impact_text = fantasy_impact.text.strip() if fantasy_impact else "No fantasy impact available."
                else:
                    fantasy_impact_text = "No fantasy impact available."

                formatted_output += (
                    f"{news_title}\n"
                    f"{summary}\n"
                    f"{fantasy_impact_text}\n\n"
                )
            return formatted_output.strip()
    return f"No news available for {player_name}."
