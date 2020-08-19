import pandas as pd
import numpy as np
import os
import re

all_projects = pd.read_csv("../dataset/all_projects_raw.csv", encoding="utf-8-sig")
all_hackathons = pd.read_csv("../dataset/all_hackathons_raw.csv", encoding="utf-8-sig")

# Remove softwares not in any hackathon
all_projects.dropna(subset=['hackathon_urls'], inplace=True)

# Fix erroneous values
to_replace = {
    "https://l.facebook.com/l.php?u=https%3A%2F%2Fgithub.com%2Fsudhirmandarapu%2Fsound-face&h=ATPPmvKAv8zmx_jQsMqOBXJZTNUQgItGdTB_qFJcXEQo4vN0KEdcYPsYQat_yh_8IYnpoMOFEXdS-zwCX5l9ztk1At-k8K_hIaxFCznJRUBNo98lcbp768jrcU80VXqKWQaJ-P8SGTkJuA" : "https://github.com/sudhirmandarapu/sound-face",
    "https://l.facebook.com/l.php?u=https%3A%2F%2Fgithub.com%2Ftoluolubode%2FMcHacks17%2Finvitations&h=ATOrMaNORxRVRs3W-z4yzwiS9aWRDNA5xB_aEXEptjatxUPm4uBjHl2MchO1hI7YqPSRXzcr3psq7CuFjVuZPZSsCPOumwW2VCJXPYhFbRgZfZY0F9vll6_ZG0Gaal0OsbSSTa6PG2s" :  "https://github.com/toluolubode/mchacks17",
    "https://l.facebook.com/l.php?u=https%3A%2F%2Fgithub.com%2Fcodepujan%2FSeeget&h=6AQEhrlvV" : "https://github.com/codepujan/Seeget",
    "https://l.facebook.com/l.php?u=https%3A%2F%2Fgithub.com%2Fakashlevy%2FWhoDatFace&h=fAQFZkxPE" : "https://github.com/akashlevy/whodatface",
    "https://www.facebook.com/l.php?u=https%3A%2F%2Fgithub.com%2Ffaizanv%2FPushing-Buttons-Backend&h=7AQH3QoDA" : "https://github.com/faizanv/pushing-buttons-backend",
    "http://goforbrokemh6.me||http://goforbroke.co||http://goforbroke.com||https://www.facebook.com/l.php?u=https%3A%2F%2Fgithub.com%2Ffaizanv%2FGo-For-Broke-Android&h=QAQECSpa9||https://github.com/faizanv/Go-For-Broke-Android" : "http://goforbrokemh6.me||http://goforbroke.co||http://goforbroke.com||https://github.com/faizanv/Go-For-Broke-Android",
    "https://l.messenger.com/l.php?u=https%3A%2F%2Fgithub.com%2Fxinyizou%2FSnapGuess&h=AT3UlS7n82zDLlO0UEK3x3L3UVRX9fP1voTGxVRG-nQgcjvlq4vspJUAmxYn1jl880cAd-_m-tznnTp0sVVBzlDkVJ1Xn-f65BSwyqPvCxostGXnRtOF8rO7hCGewLGzCzuy7NiMBZgh7qocljuuIQ" : "https://github.com/xinyizou/snapguess",
    "https://l.messenger.com/l.php?u=https%3A%2F%2Fgithub.com%2Fjwyterlin%2Fsocialfvs&h=AT0XPhnl4fAJDoXAaphqXVWbO5lO51xydOWS2mZ416vBfa6neIrf2kL4T-R2I0hbeEdDpOYCREKPEgs-j0kGLUYXq07Vpebe50P24pQEV6CncdKg3Q8ET3KgUNi7jNyGIwHOMOwMnQvRqiugZArt5A" : "https://github.com/jwyterlin/socialfvs",
    "https://github.com/YuvalFatal/Coffee-Break#coffee-break" : "https://github.com/YuvalFatal/Coffee-Break",
    "https://github.com/Codi257/oru-innovationVI#oru-innovationvi||http://homeaze.000webhostapp.com/||https://homeaze.000webhostapp.com/homepage.html||https://homeaze.000webhostapp.com/reservation.html||https://homeaze.000webhostapp.com/shelterpage.html" : "https://github.com/Codi257/oru-innovationVI||http://homeaze.000webhostapp.com/||https://homeaze.000webhostapp.com/homepage.html||https://homeaze.000webhostapp.com/reservation.html||https://homeaze.000webhostapp.com/shelterpage.html",
    "https://github.com/jrigassio/Educator#educator" : "https://github.com/jrigassio/Educator",
    "https://github.com/TejpalSingh/WayWeather1#android" : "https://github.com/TejpalSingh/WayWeather1",
    "https://github.com/JustinReiter/Short-Cut#short-cut" : "https://github.com/JustinReiter/Short-Cut",
    "https://github.com/Abhishekbhagwat/Melody||https://github.com/Abhishekbhagwat/melodyMessenger#melodymessenger" : "https://github.com/Abhishekbhagwat/Melody||https://github.com/Abhishekbhagwat/melodyMessenger",
    "https://github.com/pandamic/BUdatathon#budatathon" : "https://github.com/pandamic/BUdatathon",
    "https://github.com/rorrorojas3/binary-translator#binary-translator" : "https://github.com/rorrorojas3/binary-translator",
    "https://github.com/mouctar19/emotionReaderBitCamp2018#bitcamp-2018---twitter-emotionsentiment-analysis" : "https://github.com/mouctar19/emotionReaderBitCamp2018",
    "https://github.com/swethasrivarnas/saavy_insights#saavy_insights||https://public.tableau.com/profile/swetha.srivarna.s#!/vizhome/SavvyInsights-PowerUpAUTOMATION/HomePage||https://github.com/swethasrivarnas/saavy_insights/blob/master/Savvy%20Insight%20-%20PowerUp%20Automation.pdf||https://www.google.co.in/search?q=saavy+insights+youtube&oq=sa&aqs=chrome.4.69i60l4j69i59l2.4918j0j4&sourceid=chrome&ie=UTF-8" : "https://github.com/swethasrivarnas/saavy_insights||https://public.tableau.com/profile/swetha.srivarna.s#!/vizhome/SavvyInsights-PowerUpAUTOMATION/HomePage||https://www.google.co.in/search?q=saavy+insights+youtube&oq=sa&aqs=chrome.4.69i60l4j69i59l2.4918j0j4&sourceid=chrome&ie=UTF-8",
    "https://github.com/K-energy/Carbonet#carbonet" : "https://github.com/K-energy/Carbonet",
    "https://github.com/SphinxNumberNine/VibeCheck#vibecheck" : "https://github.com/SphinxNumberNine/VibeCheck"
}
all_projects = all_projects.replace({"software_url" : to_replace})

# drop hackathons that have not ended at the moment
all_hackathons = all_hackathons[all_hackathons.is_ended == True]

# Write projects
output = "../dataset/all_projects_cleaned.csv"
if os.path.exists(output):
    os.remove(output)
all_projects.to_csv(output, encoding='utf-8-sig', index=False)

# Write hackathons
output = "../dataset/all_hackathons_cleaned.csv"
if os.path.exists(output):
    os.remove(output)
all_hackathons.to_csv(output, encoding='utf-8-sig', index=False)