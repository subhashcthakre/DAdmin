import io
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="District Intelligence Portal - Balaghat Collectorate",
    page_icon="🏛️",
    layout="wide",
)

# --- COMPLETE OFFICER DIRECTORY & ACCESS CONTROL (112 Officials) ---
ADMIN_UPL_EMAILS = [
    "loksevabalaghat@gmail.com",
    "dmbalaghat@nic.in",
    "dio-bgt@nic.in",
]

OFFICER_DIRECTORY = {
    "dmbalaghat@nic.in": "DM Balaghat / OIC Establishment / OIC Reader",
    "loksevabalaghat@gmail.com": "Anil Kumar Lilhare (DMPSM)",
    "actw.bgt@mp.gov.in": "SM. Sakuntla Damour (AC Tribal)",
    "handloomwaraseoni@gmail.com": "Vinayak Singh Marko (AD Handloom)",
    "hortbalaghat@gmail.com": "Kshitij Karhade (AD Horticulture)",
    "admbalaghat@mp.gov.in": "D P Burnman (ADM / Dy DEO General)",
    "admbaihar@gmail.com": "D P Burnman (ADM Baihar)",
    "gs.dhurbe@mp.gov.in": "Smt. Manjula Shendre (AD OBC)",
    "balaghat.serimp@gmail.com": "Surendra Singh Chicham (AD Sericulture)",
    "dm-chhindwara@mp.gov.in": "Deepak Ade (AGM MPRDC)",
    "daoblgt.mp@mp.gov.in": "Dr Savedita Kumre (AYUSH)",
    "cbsbalaghat.mp@gmail.com": "Purushottam Joshi (CEO CCB)",
    "jpbaibal@mp.nic.in": "B S Maravi (CEO JP Baihar)",
    "jpbalaghat@mp.nic.in": "Mamta Kulaste (CEO JP Balaghat & Kirnapur)",
    "jpbirbal@mp.nic.in": "Nitin Bhatt (CEO JP Birsa)",
    "jpkatbal@mp.nic.in": "Gayatri Kumar Sarthi (CEO JP Katangi)",
    "jpkhabal@mp.nic.in": "Diksha Jain (CEO JP Khairlanji)",
    "jplalbal@mp.nic.in": "Chandar Singh Mandole (CEO JP Lalbarra)",
    "jplanbal@mp.nic.in": "Ankit Singhai (CEO JP Lanji)",
    "jpparbal@mp.gov.in": "Dhanaram Uikey (CEO JP Paraswada)",
    "jpwarbal@mp.nic.in": "Vandana Kushram (CEO JP Waraseoni)",
    "ceozpbal@mp.gov.in": "Ms. Tanushri Meena (CEO ZP Balaghat)",
    "csurgeonbalmp@mp.nic.in": "Dr. Nilay Jain (Civil Surgeon)",
    "cmhobal@mp.nic.in": "Dr. Satrudhan Dahiya (CMHO)",
    "cmobaihar@mpurban.gov.in": "Hitesh Halmare (CMO Baihar)",
    "cmokatangibalaghat@mpurban.gov.in": "Radheshyam Choudhary (CMO Katangi)",
    "cmolanji@mpurban.gov.in": "Mayur Wahane (CMO Lanji)",
    "cmomalajkhand@mpurban.gov.in": "Dinesh Baghmare (CMO Malajkhand)",
    "cmobalaghat@mpurban.gov.in": "Shri Surya Parkash Uke (CMO Nagarpalika Balaghat)",
    "cmowaraseoni@mpurban.gov.in": "Suryaprakash Uke (CMO Waraseoni)",
    "cmrisebalaghat@gmail.com": "Yuvraj Rahangdale (CMRISE Principal)",
    "ddagribal@mp.gov.in": "Mr. Phool Singh Malviya (DD Agriculture)",
    "ddfishbal@mp.gov.in": "Pooja Rodge (DD Fisheries)",
    "ddvs.ahbal@mp.gov.in": "Dr. Ghansyam Parte (DDVS)",
    "degmbal@mp.gov.in": "Vivek Meshram (DEGM Egov)",
    "deobal-mp@nic.in": "Smt. Dhanshri Jain (DEO Balaghat)",
    "deo.mpedbgt@mp.gov.in": "Ajeet Ekka (DEO Excise)",
    "pswbal@gmail.com": "Abhishekh Saraf (Deputy Director Social)",
    "fotnbghat@mp.gov.in": "Resham Singh Dhurve (DFO North)",
    "fotsbghat@mp.gov.in": "Mr. Nithiyanantham L. (DFO South)",
    "dio-bgt@nic.in": "Subhash Chandra Thakre (DIO NIC)",
    "drbalaghat@gmail.com": "Mrs. Keerti Asati (District Registrar)",
    "dmobalaghat.mp@gmail.com": "Vivek Tiwari (DMO Markfed)",
    "zskbalaghat2@gmail.com": "Shri G-S Barman (DPC ZSK)",
    "srlm-balaghat@mp.gov.in": "Shweta Mehto (DPM NRLM)",
    "dpobalaghat@rediffmail.com": "Shri Deepak Rana (DPO Pension & Treasury)",
    "dpobal@mp.gov.in": "Yashwant Vaidya (DPO Planning & WCD)",
    "drcoop.bgt@mp.gov.in": "Rajesh Uikey (DR Cooperative)",
    "foodoffbal@mp.nic.in": "Sant Kumar Bhalavi (DSO Food)",
    "dsobalaghat12@gmail.com": "Rahul Baresa (DSO Sport)",
    "deobalaghat@gmail.com": "D.P Barman (Dy DEO General)",
    "deephedbal@nic.in": "B.L. Uikey (EE PHE)",
    "eepwd1blgt@mp.nic.in": "Shri B S Adme (EE PWD)",
    "dpepiubalaghat@gmail.com": "B.S. Adme (EE PWD Building)",
    "eeresbalaghat@mp.gov.in": "Miter Kumar Ekka / Manoj Kumar Dhurvey (EE RES)",
    "ee.wrsurveydn@gmail.com": "Shri Uday Singh Parte (EE WRD Survey)",
    "eewdnbgt08@gmail.com": "Y. S. Thakur (EE WRD Wainganga)",
    "hegknacbal@mp.gov.in": "Dr Nidhi Thakur (Girls College)",
    "gmibal@mp.nic.in": "Preeti Marskole (GM DIC)",
    "gm_bgtpiu1@rediffmail.com": "Tovindra Singh Johare (GM MPRRDA PIU1)",
    "gm_bgtpiu.2@rediffmail.com": "Smt. Maya Manish Parte (GM MPRRDA PIU 2)",
    "inspwmbgt12@gmail.com": "Rajkumar Kachhwaha (Inspector Naptol)",
    "gmmandla.jalnigam@mpjalnigam.mp.gov.in": "Mr Hemant Jindwani (Jal Nigam)",
    "hegjtcbal@mp.gov.in": "Dr Ashok Kumar Marathe (JSTPG College)",
    "lobalaghat@mp.gov.in": "Shri Rakesh Thakre (Labour Officer)",
    "ldmbalag@centralbank.co.in": "Sanjeev Kumar (LDM)",
    "modgmbal@mp.gov.in": "Farhat Jahan (Mining Officer)",
    "tahsil.lamta@gmail.com": "Mayank Mishra (NT Lamta)",
    "asrbgt@gmail.com": "Shri Sudhir Jain (OIC ASR)",
    "reliefbgt@gmail.com": "Shri Sudhir Jain (OIC CM Relief Fund)",
    "oiccomplaint@gmail.com": "Shri Sudhir Jain (OIC Complaint)",
    "dmfbalaghat@gmail.com": "Manoj Kumar Dhurwey (OIC DMF)",
    "r95545812@gmail.com": "Shri Sudhir Jain (OIC Jan Shikayat)",
    "pandey.rajiv65@gmail.com": "Shri Sudhir Jain (OIC Najul)",
    "nakalbgt@gmail.com": "Shri Sudhir Jain (OIC Nakal)",
    "kol.mayaram@gmail.com": "Rahul Nayak (OIC Rahat)",
    "scbalaghat@gmail.com": "Shri Sudhir Jain (OIC SC Section)",
    "oicsw@gmail.com": "G S Dhurwe (OIC SW)",
    "podudabalaghat@mpurban.gov.in": "Mr Rahul Nayak (PO Duda)",
    "prinpoly.bgt@mp.gov.in": "R.M Sonway (Polytechnic Principal)",
    "balaghatiti@gmail.com": "Sapna Choudhary (Principal ITI)",
    "sdopwdbri@gmail.com": "A.S Sanodiya (PWD Bridge)",
    "dreobalaghat.mpuvn1982@gmail.com": "Prince Kesharwani (Renewable Energy)",
    "animesha123@gmail.com": "Shri Devesh Batham (RTO)",
    "sdmbgtbai@gmail.com": "Shri Aniket Shandilya (SDM Baihar)",
    "sdmbgt@gmail.com": "Gopal Soni (SDM Balaghat)",
    "sdmkatangi@gmail.com": "Shri Vijay Singh Yadav (SDM Katangi)",
    "sdmofficekirnapur@gmail.com": "Shri Kamalchandra Singh Sar (SDM Kirnapur)",
    "sdmbgtlan@gmail.com": "Shri Aditya Narayan Tiwari (SDM Lanji)",
    "sdmparaswada@gmail.com": "Shrish Pyasi (SDM Paraswada)",
    "waraseonisdm@gmail.com": "Shrish Pyasi (SDM Waraseoni)",
    "sebalaghat@gmail.com": "Deepak Kumar Uikey (SE MPEB)",
    "slrbal@mp.gov.in": "Shri Krishna Nayak (SLR)",
    "sp_balaghat@mppolice.gov.in": "Shri Aaditya Mishra (SP Balaghat)",
    "sgtbalaghat7@gmail.com": "Ramesh Gohe (Sr Geohydrologist)",
    "tdbaihar@gmail.com": "Anurag Singh Maravi (TD Baihar)",
    "tdbalaghat@gmail.com": "Chhvi Pant (TD Balaghat)",
    "tahbirsa@gmail.com": "Babita Surya (TD Birsa)",
    "tdkatangi@gmail.com": "P L Sandiya (TD Katangi)",
    "tahbgtkha@gmail.com": "Teerath Prasad Aksharya (TD Khairlanji)",
    "tdkirnapur@gmail.com": "Varsha Jhariya (TD Kirnapur)",
    "tahbgtlal17@gmail.com": "Bhupendra Ahirwar (TD Lalbarra)",
    "tdlanji@gmail.com": "Himmatsingh Bhawedi (TD Lanji)",
    "tahbgtpar@gmail.com": "Kanhaiyalal Tekam (TD Paraswada)",
    "tdtirodi@gmail.com": "Geeta Rahangdale (TD Tirodi)",
    "tdwaraseoni@gmail.com": "Vandana Kushram (TD Waraseoni)",
    "tobalaghat@rediffmail.com": "Shri Deepak Rana (Treasury Officer)",
}


def check_auth():
  st.sidebar.markdown("---")
  st.sidebar.subheader("🔐 Officer Login")
  user_email = st.sidebar.text_input(
      "Enter your official email:", placeholder="name@nic.in / @mp.gov.in"
  )

  if not user_email:
    st.warning("⚠️ Please enter your official department email in the sidebar.")
    st.stop()

  user_email = user_email.strip().lower()

  if user_email in ADMIN_UPL_EMAILS:
    return "Admin", user_email
  elif user_email in OFFICER_DIRECTORY or user_email.endswith(
      ("@mp.gov.in", "@nic.in", "@mpurban.gov.in")
  ):
    return "Viewer", user_email
  else:
    st.error(
        f"❌ Access Denied: '{user_email}' is not registered in the District"
        " Officer Directory."
    )
    st.stop()


role, current_user = check_auth()
officer_title = OFFICER_DIRECTORY.get(current_user, "District Officer")

# --- HEADER ---
st.title("🏛️ District Administration Intelligence Portal - Balaghat")
st.markdown(
    "*Zero-Cost Decision Support System for Collectorate Review Meetings*"
)
st.sidebar.info(
    f"👤 **User:** `{current_user}`\n\n🏷️ **Office:** {officer_title}\n\n🛡️"
    f" **Role:** **{role}**"
)

# --- NAVIGATION MODULES ---
st.sidebar.markdown("---")
st.sidebar.subheader("📂 Modules")
module = st.sidebar.radio(
    "Select Module",
    [
        "📊 Time Limit (TL) Letters",
        "📞 Jansunwai Tracker",
        "🗺️ Geo-Drilldown & GIS Map",
        "📋 Weekly TL Meeting Agenda",
    ],
)

# --- SESSION STATE INITIALIZATION ---
if "tl_df" not in st.session_state:
  sample_data = {
      "S.No": [1, 2, 3, 4, 5, 6, 7, 8],
      "Sub-Division": [
          "Balaghat",
          "Balaghat",
          "Katangi",
          "Balaghat",
          "Baihar",
          "Waraseoni",
          "Kirnapur",
          "Lanji",
      ],
      "Tahsil": [
          "Balaghat",
          "Balaghat",
          "Katangi",
          "Balaghat",
          "Baihar",
          "Waraseoni",
          "Kirnapur",
          "Lanji",
      ],
      "Block": [
          "Balaghat",
          "Balaghat",
          "Katangi",
          "Balaghat",
          "Baihar",
          "Waraseoni",
          "Kirnapur",
          "Lanji",
      ],
      "Name of Office": [
          "ADM",
          "CEO ZP BALAGHAT",
          "CMHO",
          "po duda",
          "SDM_Baihar",
          "SDM_Waraseoni",
          "SE MPEB",
          "TD_Lanji",
      ],
      "Received Letters": [120, 95, 150, 60, 45, 80, 110, 70],
      "Disposed Letters": [100, 85, 120, 50, 40, 65, 90, 55],
      "Pending Letters": [20, 10, 30, 10, 5, 15, 20, 15],
      "Not Replied Letters": [5, 2, 8, 3, 1, 4, 6, 5],
      "Out of Time Limit": [3, 1, 5, 2, 0, 3, 4, 2],
  }
  st.session_state.tl_df = pd.DataFrame(sample_data)

if "jansunwai_df" not in st.session_state:
  js_data = {
      "S.No": [1, 2, 3, 4, 5],
      "Tahsil": ["Balaghat", "Katangi", "Waraseoni", "Baihar", "Lanji"],
      "Department": ["Revenue", "Panchayat", "Health", "Police", "Food"],
      "Received Grievances": [45, 30, 25, 40, 20],
      "Resolved": [40, 25, 20, 32, 15],
      "Pending": [5, 5, 5, 8, 5],
      "Escalated (>15 Days)": [1, 2, 0, 3, 1],
  }
  st.session_state.jansunwai_df = pd.DataFrame(js_data)

# --- MODULE 1: TIME LIMIT (TL) LETTERS ---
if module == "📊 Time Limit (TL) Letters":
  st.header("📊 Time Limit (TL) Letters - Department Dashboard")
  st.markdown(
      "Monitor departmental disposal efficiency, pending references, and"
      " out-of-time-limit files."
  )

  if role == "Admin":
    with st.expander("📤 Upload New Jan Akansha Excel Report"):
      uploaded_file = st.file_uploader(
          "Upload Excel (.xlsx)", type=["xlsx", "xls"]
      )
      if uploaded_file is not None:
        try:
          raw_df = pd.read_excel(uploaded_file, header=1)
          st.success("Jan Akansha Excel file successfully parsed!")
          st.dataframe(raw_df.head(3))
        except Exception as e:
          st.error(f"Error reading file: {e}")

  df = st.session_state.tl_df.copy()
  df["Dispos %"] = (
      (df["Disposed Letters"] / df["Received Letters"]) * 100
  ).round(2)

  col1, col2, col3, col4, col5 = st.columns(5)
  col1.metric("Total Received", int(df["Received Letters"].sum()))
  col2.metric("Total Disposed", int(df["Disposed Letters"].sum()))
  col3.metric("Total Pending", int(df["Pending Letters"].sum()))
  col4.metric("Not Replied", int(df["Not Replied Letters"].sum()))
  col5.metric(
      "Avg Disposal %", f"{df['Dispos %'].mean():.1f}%"
  )

  st.markdown("---")
  search_office = st.text_input("🔍 Search Office / Department")
  if search_office:
    df = df[
        df["Name of Office"].str.contains(search_office, case=False, na=False)
    ]

  st.subheader("Department-wise Performance Table")
  st.dataframe(df, use_container_width=True)

# --- MODULE 2: JANSUNWAI TRACKER ---
elif module == "📞 Jansunwai Tracker":
  st.header("📞 Jansunwai Grievance Management Dashboard")
  st.markdown(
      "Track weekly district public hearing grievances, category-wise"
      " pendency, and escalation status."
  )

  js_df = st.session_state.jansunwai_df.copy()
  js_df["Resolution %"] = (
      (js_df["Resolved"] / js_df["Received Grievances"]) * 100
  ).round(2)

  c1, c2, c3 = st.columns(3)
  c1.metric("Total Grievances", int(js_df["Received Grievances"].sum()))
  c2.metric("Total Resolved", int(js_df["Resolved"].sum()))
  c3.metric("Total Escalated", int(js_df["Escalated (>15 Days)"].sum()))

  st.markdown("---")
  st.dataframe(js_df, use_container_width=True)

# --- MODULE 3: GEO-DRILLDOWN & GIS MAP ---
elif module == "🗺️ Geo-Drilldown & GIS Map":
  st.header("🗺️ Administrative Geographic Drill-Down & GIS Map")
  st.markdown(
      "Filter all district parameters instantly when visiting Sub-Divisions,"
      " Tahsils, or Blocks, and view interactive district map."
  )

  col1, col2, col3 = st.columns(3)
  with col1:
    sel_sub = st.selectbox(
        "Select Sub-Division",
        [
            "All",
            "Balaghat",
            "Baihar",
            "Waraseoni",
            "Katangi",
            "Kirnapur",
            "Lanji",
            "Paraswada",
        ],
    )
  with col2:
    sel_tahsil = st.selectbox(
        "Select Tahsil",
        [
            "All",
            "Balaghat",
            "Lamta",
            "Baihar",
            "Birsa",
            "Katangi",
            "Tirodi",
            "Waraseoni",
            "Khairlanji",
            "Lalbarra",
            "Kirnapur",
            "Lanji",
            "Paraswada",
        ],
    )
  with col3:
    sel_block = st.selectbox(
        "Select Block",
        [
            "All",
            "Balaghat",
            "Baihar",
            "Birsa",
            "Katangi",
            "Khairlanji",
            "Lalbarra",
            "Kirnapur",
            "Lanji",
            "Paraswada",
            "Waraseoni",
        ],
    )

  st.success(
      f"Active Geo Filter — Sub-Division: **{sel_sub}** | Tahsil:"
      f" **{sel_tahsil}** | Block: **{sel_block}**"
  )

  # Interactive Free Leaflet Map centered on Balaghat Collectorate
  st.subheader("📍 Balaghat District Interactive Map Viewer (Free OpenStreetMap)")
  m = folium.Map(location=[21.8024, 80.1856], zoom_start=10)

  # Add key administrative pins
  folium.Marker(
      [21.8024, 80.1856],
      popup="District Collectorate Balaghat",
      tooltip="Collectorate HQ",
  ).add_to(m)
  folium.Marker(
      [22.1000, 80.5500],
      popup="SDM Office / Tehsil Baihar",
      tooltip="Baihar Sub-Division",
  ).add_to(m)
  folium.Marker(
      [21.7700, 80.0500],
      popup="SDM Office / Tehsil Waraseoni",
      tooltip="Waraseoni Sub-Division",
  ).add_to(m)
  folium.Marker(
      [21.7800, 79.8000],
      popup="SDM Office / Tehsil Katangi",
      tooltip="Katangi Sub-Division",
  ).add_to(m)
  folium.Marker(
      [21.5500, 80.2500],
      popup="SDM Office / Tehsil Lanji",
      tooltip="Lanji Sub-Division",
  ).add_to(m)

  st_folium(m, width=1100, height=450)

# --- MODULE 4: WEEKLY TL MEETING AGENDA ---
elif module == "📋 Weekly TL Meeting Agenda":
  st.header("📋 Collector's Weekly Time Limit (TL) Meeting Agenda")
  st.markdown(
      "Review weekly agenda points, Samagra e-KYC progress, Ayushman cards,"
      " and pending dues."
  )

  # Samagra e-KYC Data Table from the document
  st.subheader("1. Samagra e-KYC District Progress (Target vs Verified)")
  ekyc_data = {
      "Block / Urban Body": [
          "Nagar Parishad, BAIHAR",
          "Nagar Parishad, KATANGI",
          "Nagar Palika, MALAJKHAND",
          "Janpad Panchayat, KHAIRLANJI",
          "Janpad Panchayat, WARA SEONI",
          "Nagar Parishad, LANJHI",
          "Janpad Panchayat, BIRSA",
          "Janpad Panchayat, BALAGHAT",
          "Nagar Palika, WARA SEONI",
          "Janpad Panchayat, LAL BURRA",
          "Janpad Panchayat, KIRNAPUR",
          "Janpad Panchayat, BAIHAR",
          "Janpad Panchayat, LANJI",
          "Janpad Panchayat, PARASWADA",
          "Janpad Panchayat, KATANGI",
          "Nagar Palika, Balaghat",
      ],
      "Total Members": [
          16302,
          15923,
          32379,
          156648,
          166529,
          14106,
          152211,
          204287,
          26307,
          191891,
          206403,
          113883,
          203818,
          122860,
          186732,
          85553,
      ],
      "e-KYC Verified": [
          16013,
          15521,
          31409,
          151423,
          159321,
          13483,
          145170,
          193589,
          24870,
          180145,
          192981,
          106257,
          190000,
          113912,
          171755,
          74607,
      ],
      "Verified %": [
          98.23,
          97.48,
          97.00,
          96.66,
          95.67,
          95.58,
          95.37,
          94.76,
          94.54,
          93.88,
          93.50,
          93.30,
          93.22,
          92.72,
          91.98,
          87.21,
      ],
  }
  st.dataframe(pd.DataFrame(ekyc_data), use_container_width=True)

  st.markdown("---")
  st.subheader("2. Key Weekly Review Agenda Summary")
  agenda_summary = {
      "Agenda Item": [
          "Ayushman Card Progress",
          "HPV Vaccination (Cervical Cancer)",
          "CM Rise Schools Construction",
          "Pending Electricity Dues (MPEB)",
          "Jal Ganga Samvardhan Abhiyan",
      ],
      "Current Status / Achievement": [
          "Target: 13,22,342 | Achievement: 13,34,750 (100.92%)",
          "460 Sessions organized; 15,720 adolescent girls vaccinated (97.46%)",
          "Completed in Landejhari, Waraseoni, Balaghat, Bolegaon, Rajegaon, Khairlanji",
          "Total outstanding: 2,198.08 Lakhs across departments & Panchayats",
          "Farm ponds (4,433/4,473), Amrit Sarovar (23/23) completed",
      ],
  }
  st.dataframe(pd.DataFrame(agenda_summary), use_container_width=True)

  if st.button("📥 Download Monday Review Briefing Report"):
    st.download_button(
        label="Download Text Brief",
        data="BALAGHAT DISTRICT COLLECTORATE - MONDAY REVIEW MEETING BRIEFING",
        file_name="Collector_Review_Brief.txt",
        mime="text/plain",
    )