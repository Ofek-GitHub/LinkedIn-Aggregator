import requests
from flask import request, jsonify
from .models import MongoDBUtility
from config import Config
from dotenv import load_dotenv, find_dotenv
import os

mongo = MongoDBUtility(
    Config.MONGO_URI,
    "AllJobs",
    "AllJobs",
)

csrf_token = os.environ.get("CSRF_TOKEN")


def get_jobs(keywords):
    fetch_options = {
        "method": "GET",
        "headers": {
            "accept": "application/vnd.linkedin.normalized+json+2.1",
            "accept-language": "en-US,en;q=0.9",
            "csrf-token": csrf_token,
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-li-deco-include-micro-schema": "true",
            "x-li-lang": "en_US",
            "x-li-page-instance": "urn:li:page:d_flagship3_search_srp_jobs;2b/k6Al6SIuzhJL7v4xDZQ==",
            "x-li-pem-metadata": "Voyager - Careers=jobs-search-results",
            "x-li-track": '{"clientVersion":"1.13.8499","mpVersion":"1.13.8499","osName":"web","timezoneOffset":2,"timezone":"Asia/Jerusalem","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1,"displayWidth":1920,"displayHeight":1080}',
            "x-restli-protocol-version": "2.0.0",
            "cookie": 'li_sugr=371fb871-b355-422b-84c5-1354416211de; bcookie="v=2&d3a02ff1-6d00-441a-8985-9320d457d8b7"; bscookie="v=1&202405121124354c4a594d-acc9-4985-85ef-e807764f83f4AQG04OItWlo8sFuNy8ciIMgkKxwwETiE"; g_state={"i_l":0}; fcookie=AQGk3myTSizAEgAAAY-bdzNKw5aQb75cevOZYdBRaA7me1i7_k1PMdBNVfGdZZSuRO_q6g2u5SlgjP-mCqXgPHOLloN7OL50fBHjgpHrrszymnY4l12k3g7QRVprjj09rQZkE8216wbVPGlqmcQ2EO1vkr7mTDZAqLgf_K_m3zdPX0Rj9AzfMZ_s-3W_R7BznwSuyTzXS15LpXRX466TQ_W65nKPDJdnOVDwuAqmi4ziB8DhxDmwR1-rBQG9p7DLnW0SChjQhQZPi6E4pkO7VoA0NOOLYVCyCeKqqsDgj3CwgVu/jqeyX4zFIzfHB/sdOtS420HL5zdrrWYQ==; li_at=AQEDATMPNmcDxKi1AAABj5t3NUEAAAGPv4O5QU0Ap7Mu5wg10PbhfR1mRDvdh96vJm49y8futP9zQTKemFeFBBpAGupPLl3i3LCdie0Ug1ed17kaqBQ7mZeWz2MOAM6th_AUJmGJiU1iIpI9vppqk6WY; liap=true; JSESSIONID="ajax:0115939538335324286"; fid=AQFQU5Dij2-AeAAAAY-bdzY6pHhlB39Q28NgR08WpCaZxUgVLibRxjcktPnVJSeiRuwZ5DaJ5rmrKg; timezone=Asia/Jerusalem; li_theme=light; li_theme_set=app; dfpfpt=7d8c9898956b4adab45616f0c2f7b7dc; AnalyticsSyncHistory=AQKOgIo51rRHAgAAAY-bd0OwOT4BLaWjc3Jxv703or1nl01rfbZ8wjJ2LCgqCgzWntfYreOoLr1cYOR18uVKAQ; _guid=3462a25c-b741-4306-8a01-399b790c4338; aam_uuid=48255832291769229634387242779442049197; lms_ads=AQEq_2IwVnOWxQAAAY-bd0RrC0R1J1wO77VMAmjaqDHFAyHzLhb9osNmrpz3_W21JREhViuicuePVHhzHTauJst1-16BiXJj; lms_analytics=AQEq_2IwVnOWxQAAAY-bd0RrC0R1J1wO77VMAmjaqDHFAyHzLhb9osNmrpz3_W21JREhViuicuePVHhzHTauJst1-16BiXJj; _gcl_au=1.1.1100267795.1716300250; lang=v=2&lang=en-us; UserMatchHistory=AQLKzf6PIqQX2wAAAY-fPgjhs_sfTBV45YxnIas8sn6Agg0LMz7jZmQMlKB868jquF49ipKCZ_2Zerd9D7DxBBakwjyaqMPVZ1d8O3Nm9gOsLAY1KHgtODUsLdmDUC9iIgKt2uXfybABnIcuQviNEyAUei-KZivjMJ9AyzwxbgGQmYIgo0E42f7cf16CE2KUUiusGY3Ndf-KoLa7m1NvtBB7jnyy22ZodHVSlrSYQHXsTHs7Al9_TDvLrCJA_DaEfQiCgAdxzKzJLdEu_wC4Pj7VPqYNAYu8ei_0oT51NvopcnsV1W8jwKIgOtD3ktJPXTmAYW2Au90R39-VsQDNl678twGBJALq_XT4wo0QV_m_F7HQ6w; fptctx2=taBcrIH61PuCVH7eNCyH0FFaWZWIHTJWSYlBtG47cVs%252fCuKz7sd0wvK0mBbcde0Rr2uupogW%252fR4NdwnuQaEDY2tPlGpQ6iJBnDcoSk9E0HRv6T4tUtwisZyKqt5t0RjviflTbNQuj486AUZtty2SGfUhAc%252f4NiUIE96N0Q7cpQWp0X%252bq3Rd7RsjIu2sawz%252bGSB%252biqtMc1z%252f5R0rWK9ErH7PpGAjzUbWDWnZU43V2BouaUT1hAFaUaBJTp6TmBk%252f49glCXrOYaigaGP%252bb2L%252b6v9u21c5oPsgOkjAoyDXaSvgw4HQqHXyzgmfL0%252fYI9kV4z113iQaQzzR571scxwU7f6sjPC9KS%252f41CxctTZbQdtM%253d; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19865%7CMCMID%7C47717808126809007604336316821062320998%7CMCAAMLH-1716968403%7C6%7CMCAAMB-1716968403%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1716370803s%7CNONE%7CMCCIDH%7C-2046541424%7CvVersion%7C5.1.1; sdsc=22%3A1%2C1716363687398%7EJAPP%2C0P7Nqzgicmd9lkdE%2BGeIhU%2FrIk5g%3D; lidc="b=TB83:s=T:r=T:a=T:p=T:g=3695:u=293:x=1:i=1716411619:t=1716413171:v=2:sig=AQH10U-3VQpdQtaTOO1KuRop2SNu1Wc1"',
            "Referer": f"https://www.linkedin.com/jobs/search/?currentJobId=3785694326&keywords={keywords}&origin=JOBS_HOME_KEYWORD_AUTOCOMPLETE&refresh=true",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        },
    }

    response = requests.get(
        f"https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollection-207&count=25&q=jobSearch&query=(origin:JOB_COLLECTION_PAGE_KEYWORD_HISTORY,keywords:{keywords},locationUnion:(geoId:101620260),selectedFilters:(distance:List(25)),spellCorrectionEnabled:true)&start=0",
        headers=fetch_options["headers"],
    )

    data = response.json()
    data1 = data["included"]
    data2 = data["data"]["paging"]
    data3 = data2["total"]
    print(data3)
    desired_property = "preDashNormalizedJobPostingUrn"
    extracted_data = []
    print(len(data1))
    for obj in data1:
        if desired_property in obj:
            extracted_data.append(obj)
            print(obj.keys())

    extracted_jobs = [
        {
            "title": item.get("jobPostingTitle", "No Title Available"),
            "location": item.get("secondaryDescription", {}).get(
                "text", "Location Not Available"
            ),
            "trackingUrn": item.get("jobPostingUrn", "No URN Available"),
        }
        for item in extracted_data
    ]
    mongo.insert_data(extracted_jobs)  # sending data to the database

    for start in range(25, data3, 25):
        response = requests.get(
            f"https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollection-207&count=25&q=jobSearch&query=(origin:JOB_COLLECTION_PAGE_KEYWORD_HISTORY,keywords:{keywords},locationUnion:(geoId:101620260),selectedFilters:(distance:List(25)),spellCorrectionEnabled:true)&start={start}",
            headers=fetch_options["headers"],
        )
        data = response.json()
        data1 = data["included"]
        data2 = data["data"]["paging"]
        data3 = data2["total"]
        print(data3)
        desired_property = "preDashNormalizedJobPostingUrn"
        extracted_data = []
        print(len(data1))
        for obj in data1:
            if desired_property in obj:
                extracted_data.append(obj)
                print(obj.keys())

        extracted_jobs = [
            {
                "title": item.get("jobPostingTitle", "No Title Available"),
                "location": item.get("secondaryDescription", {}).get(
                    "text", "Location Not Available"
                ),
                "trackingUrn": item.get("jobPostingUrn", "No URN Available"),
            }
            for item in extracted_data
        ]
        mongo.insert_data(extracted_jobs)  # sending data to the database

    return str(data2["total"])
