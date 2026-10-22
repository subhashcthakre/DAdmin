import os
import io
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="District Intelligence Portal - Balaghat Collectorate",
    page_icon="🏛️",
    layout="wide",
)

# --- UPLOAD ADMIN CONFIGURATION ---
ADMIN_UPL_EMAILS = [
    "loksevabalaghat@gmail.com",
    "dmbalaghat@nic.in",
    "dio-bgt@nic.in",
]

# --- 112 अधिकारी डायरेक्टरी ---
OFFICER_DIRECTORY = {
    "dmbalaghat@nic.in": "DM Balaghat / OIC Establishment / OIC Reader",
    "loksevabalaghat@gmail.com": "Anil Kumar Lilhare (DMPSM)",
    "actw.bgt@mp.gov.in": "SM. Sakuntla Damour (AC Tribal)",
    "handloomwaraseoni@gmail.com": "Vinayak Singh Marko (AD Handloom)",
    "hortbalaghat@gmail.com": "Kshitij Karhade (AD Horticulture)",
    "admbalaghat@mp.gov.in": "D P Burnman (ADM / Dy DEO General)",
    "admbaihar@mp.gov.in": "D P Burnman (ADM Baihar)",
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
    "dmobalaghat.mp.gmail.com": "Vivek Tiwari (DMO Markfed)",
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
    "tahbgtkha@gmail.com": "Teerath Prasad Aksharya (Tahsildar Khairlanji)",
    "tdkirnapur@gmail.com": "Varsha Jhariya (TD Kirnapur)",
    "tahbgtlal17@gmail.com": "Bhupendra Ahirwar (TD Lalbarra)",
    "tdlanji@gmail.com": "Himmatsingh Bhawedi (TD Lanji)",
    "tahbgtpar@gmail.com": "Kanhaiyalal Tekam (TD Paraswada)",
    "tdtirodi@gmail.com": "Geeta Rahangdale (TD Tirodi)",
    "tdwaraseoni@gmail.com": "Vandana Kushram (TD Waraseoni)",
    "tobalaghat@rediffmail.com": "Shri Deepak Rana (Treasury Officer)",
}

# --- SECURE LOGIN SYSTEM ---
if "authenticated" not in st.session_state:
  st.session_state.authenticated = False
  st.session_state.user_email = ""
  st.session_state.user_role = ""

if not st.session_state.authenticated:
  st.markdown(
      "<h2 style='text-align: center;'>🏛️ Balaghat District Administration"
      " Portal</h2>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='text-align: center;'><b>Secure Login for Authorized District"
      " Officers</b></p>",
      unsafe_allow_html=True,
  )

  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
    with st.form("login_form"):
      email_input = st.text_input(
          "Official Email ID", placeholder="e.g. dio-bgt@nic.in"
      )
      password_input = st.text_input(
          "Password", type="password", placeholder="Enter password"
      )
      submit_button = st.form_submit_button("Secure Login")

      if submit_button:
        email_clean = email_input.strip().lower()
        if password_input == "Balaghat@2026":
          if email_clean in ADMIN_UPL_EMAILS:
            st.session_state.authenticated = True
            st.session_state.user_email = email_clean
            st.session_state.user_role = "Admin"
            st.rerun()
          elif email_clean in OFFICER_DIRECTORY or email_clean.endswith(
              ("@mp.gov.in", "@nic.in", "@mpurban.gov.in")
          ):
            st.session_state.authenticated = True
            st.session_state.user_email = email_clean
            st.session_state.user_role = "Viewer"
            st.rerun()
          else:
            st.error(
                "❌ Access Denied: Email not registered in District Directory."
            )
        else:
          st.error("❌ Incorrect Password. (Default setup password: Balaghat@2026)")
  st.stop()

# --- AUTHENTICATED SESSION ---
current_user = st.session_state.user_email
role = st.session_state.user_role
officer_title = OFFICER_DIRECTORY.get(current_user, "District Officer")

st.title("🏛️ District Administration Intelligence Portal - Balaghat")
st.markdown(
    "*Zero-Cost Decision Support System for Collectorate Review Meetings*"
)

st.sidebar.info(
    f"👤 **User:** `{current_user}`\n\n🏷️ **Office:** {officer_title}\n\n🛡️"
    f" **Role:** **{role}**"
)

if st.sidebar.button("🚪 Logout"):
  st.session_state.authenticated = False
  st.session_state.user_email = ""
  st.session_state.user_role = ""
  st.rerun()

# --- NAVIGATION MODULES ---
st.sidebar.markdown("---")
st.sidebar.subheader("📂 Modules")
module = st.sidebar.radio(
    "Select Module",
    [
        "📊 Time Limit (TL) Letters & Office Tiles",
        "📞 Jansunwai Tracker",
        "🗺️ Geo-Drilldown & GIS Map",
        "📋 Weekly TL Meeting Agenda",
    ],
)

DATA_FILE = "latest_tl_data.csv"

# Load persistent data or default sample data
if "tl_df" not in st.session_state:
  if os.path.exists(DATA_FILE):
    st.session_state.tl_df = pd.read_csv(DATA_FILE)
  else:
    sample_data = {
        "S.No": [1, 2, 3, 4, 5, 6, 7, 8],
        "Present Office": [
            "CMHO (Health)",
            "DEO (Education)",
            "CEO ZP Balaghat",
            "EE PWD",
            "EE PHE",
            "EE RES",
            "DPO WCD",
            "DDA Agriculture",
        ],
        "Marked Date": [
            "10/01/2026",
            "15/02/2026",
            "01/03/2026",
            "20/01/2026",
            "10/02/2026",
            "05/03/2026",
            "15/01/2026",
            "01/02/2026",
        ],
        "TL Date": [
            "25/01/2026",
            "28/02/2026",
            "15/03/2026",
            "05/02/2026",
            "25/02/2026",
            "20/03/2026",
            "01/02/2026",
            "15/02/2026",
        ],
        "Total Cases": [120, 95, 150, 60, 45, 80, 110, 70],
        "Replied Cases": [100, 80, 140, 45, 35, 75, 90, 60],
        "Pending Cases": [20, 15, 10, 15, 10, 5, 20, 10],
        "Disposed Cases": [100, 80, 140, 45, 35, 75, 90, 60],
        "Time Limit Over Cases": [3, 5, 1, 6, 2, 0, 4, 2],
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

# --- MODULE 1: TIME LIMIT LETTERS & OFFICE-WISE ANALYTICS TILES ---
if module == "📊 Time Limit (TL) Letters & Office Tiles":
  st.header("📊 Department & Office-wise TL Performance Analytics")
  st.markdown(
      "Filter cases by date and view comprehensive office-wise analytical"
      " tiles."
  )

  if role == "Admin":
    with st.expander("📤 Upload Real-Time Excel Report", expanded=False):
      uploaded_file = st.file_uploader(
          "Upload Jan Akansha Excel File (.xlsx)", type=["xlsx", "xls"]
      )
      if uploaded_file is not None:
        try:
          raw_df = pd.read_excel(uploaded_file, header=1)
          raw_df.to_csv(DATA_FILE, index=False)
          st.session_state.tl_df = raw_df
          st.success("✅ File uploaded and synced across all dashboards!")
        except Exception as e:
          st.error(f"Error: {e}")

  df = st.session_state.tl_df.copy()

  # --- DATE PICKER FILTER (कब से देखना है) ---
  st.markdown("---")
  col_d1, col_d2 = st.columns(2)
  with col_d1:
    from_date = st.date_input(
        "📅 From Date (कब से देखना है):",
        value=datetime.date(2026, 1, 1),
        format="YYYY-MM-DD",
    )
  with col_d2:
    to_date = st.date_input(
        "📅 To Date (कब तक):",
        value=datetime.date.today(),
        format="YYYY-MM-DD",
    )

  office_col = None
  for col_cand in ["Present Office", "Name of Office", "Office", "Department"]:
    if col_cand in df.columns:
      office_col = col_cand
      break

  # dayfirst=True का उपयोग ताकि DD/MM/YYYY सही से पार्स हो सके
  if "Marked Date" in df.columns and office_col:
    df["Parsed_Date"] = pd.to_datetime(
        df["Marked Date"], errors="coerce", dayfirst=True
    ).dt.date
    filtered_df = df[
        (df["Parsed_Date"] >= from_date) & (df["Parsed_Date"] <= to_date)
    ]
  else:
    filtered_df = df

  st.info(
      f"🔍 Showing analytics from **{from_date}** to **{to_date}** | Total"
      f" Filtered Records: `{len(filtered_df)}`"
  )

  # --- AGGREGATE METRICS FOR GIST ---
  total_cases_sum = (
      filtered_df["Total Cases"].sum()
      if "Total Cases" in filtered_df.columns
      else len(filtered_df)
  )
  total_pending_sum = (
      filtered_df["Pending Cases"].sum()
      if "Pending Cases" in filtered_df.columns
      else 0
  )
  total_oot_sum = (
      filtered_df["Time Limit Over Cases"].sum()
      if "Time Limit Over Cases" in filtered_df.columns
      else 0
  )

  c1, c2, c3 = st.columns(3)
  c1.metric("📦 Filtered Total Cases", int(total_cases_sum))
  c2.metric("⏳ Total Pending Cases", int(total_pending_sum))
  c3.metric(
      "🚨 Time Limit Over (Red Alert)",
      int(total_oot_sum),
      delta="Critical",
      delta_color="inverse",
  )

  st.markdown("---")
  st.subheader(
      "🏢 Office-wise Analytics Tiles (कार्यालय-वार विश्लेषणात्मक टाइल्स)"
  )

  if office_col:
    if "Total Cases" not in filtered_df.columns:
      office_summary = (
          filtered_df.groupby(office_col)
          .agg(
              Total_Cases=(office_col, "count"),
              Pending_Cases=(office_col, "count"),
              Disposed_Cases=(office_col, "count"),
              Replied_Cases=(office_col, "count"),
              TL_Over=(office_col, "count"),
          )
          .reset_index()
      )
    else:
      office_summary = (
          filtered_df.groupby(office_col)
          .agg(
              Total_Cases=("Total Cases", "sum"),
              Replied_Cases=("Replied Cases", "sum")
              if "Replied Cases" in filtered_df.columns
              else (office_col, "count"),
              Pending_Cases=("Pending Cases", "sum")
              if "Pending Cases" in filtered_df.columns
              else (office_col, "count"),
              Disposed_Cases=("Disposed Cases", "sum")
              if "Disposed Cases" in filtered_df.columns
              else (office_col, "count"),
              TL_Over=("Time Limit Over Cases", "sum")
              if "Time Limit Over Cases" in filtered_df.columns
              else (office_col, "count"),
          )
          .reset_index()
      )

    num_cols = 3
    rows = [
        office_summary.iloc[i : i + num_cols]
        for i in range(0, len(office_summary), num_cols)
    ]

    for row_chunk in rows:
      cols = st.columns(num_cols)
      for idx, (_, row) in enumerate(row_chunk.iterrows()):
        off_name = row[office_col]
        tot = row["Total_Cases"]
        rep = row["Replied_Cases"]
        pend = row["Pending_Cases"]
        disp = row["Disposed_Cases"]
        oot = row["TL_Over"]

        with cols[idx]:
          border_color = "red" if oot > 0 else "#2ecc71"
          st.markdown(
              f"""
                    <div style="padding: 15px; border-radius: 8px; border: 2px solid {border_color}; background-color: #1e1e1e; margin-bottom: 15px;">
                        <h4 style="margin: 0; color: #ffffff; font-size: 16px;">{off_name}</h4>
                        <hr style="margin: 5px 0 8px 0; border-color: #444;">
                        <p style="margin: 2px 0; color: #cfcfcf; font-size: 13px;">📦 Total Cases: <b>{tot}</b></p>
                        <p style="margin: 2px 0; color: #3498db; font-size: 13px;">✅ Replied: <b>{rep}</b></p>
                        <p style="margin: 2px 0; color: #2ecc71; font-size: 13px;">🎯 Disposed: <b>{disp}</b></p>
                        <p style="margin: 2px 0; color: #ffa500; font-size: 13px;">⏳ Pending: <b>{pend}</b></p>
                        <p style="margin: 2px 0; color: {'#ff4b4b' if oot > 0 else '#2ecc71'}; font-size: 13px;">🚨 TL Over: <b>{oot}</b></p>
                    </div>
                    """,
              unsafe_allow_html=True,
          )
  else:
    st.warning("⚠️ Office column not detected for generating analytical tiles.")

  st.markdown("---")
  st.subheader("📋 Filtered Detailed Data Table")
  st.dataframe(filtered_df, use_container_width=True)

# --- MODULE 2: JANSUNWAI TRACKER ---
elif module == "📞 Jansunwai Tracker":
  st.header("📞 Jansunwai Grievance Management Gist")
  js_df = st.session_state.jansunwai_df.copy()

  c1, c2, c3 = st.columns(3)
  c1.metric("Total Grievances", int(js_df["Received Grievances"].sum()))
  c2.metric("Total Resolved", int(js_df["Resolved"].sum()))
  c3.metric(
      "Escalated (>15 Days)",
      int(js_df["Escalated (>15 Days)"].sum()),
      delta="Critical",
      delta_color="inverse",
  )

  st.markdown("---")
  st.dataframe(js_df, use_container_width=True)

# --- MODULE 3: GEO-DRILLDOWN & GIS MAP ---
elif module == "🗺️ Geo-Drilldown & GIS Map":
  st.header("🗺️ Administrative Geographic Drill-Down & GIS Map")
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

  m = folium.Map(location=[21.8024, 80.1856], zoom_start=10)
  folium.Marker(
      [21.8024, 80.1856], popup="District Collectorate Balaghat"
  ).add_to(m)
  st_folium(m, width=1100, height=430)

# --- MODULE 4: WEEKLY TL MEETING AGENDA ---
elif module == "📋 Weekly TL Meeting Agenda":
  st.header("📋 Collector's Weekly Time Limit (TL) Meeting Agenda Gist")
  st.markdown(
      "Review key weekly focus points, Samagra e-KYC progress, and Red Alerts."
  )

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
          "Nagar Palika, Balaghat (⚠️ RED ALERT)",
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

  if st.button("📥 Download Monday Review Briefing Report"):
    st.download_button(
        label="Download Text Brief",
        data="BALAGHAT DISTRICT COLLECTORATE - MONDAY REVIEW MEETING BRIEFING",
        file_name="Collector_Review_Brief.txt",
        mime="text/plain",
    )