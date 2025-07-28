#  Kenya Immunization Dashboard (2022)

An interactive **Streamlit dashboard** visualizing immunization coverage across all 47 counties in Kenya.

**Live Demo**: [Click here to view the dashboard](https://wanyua-kenya-immunization-2022-dashboard-v1.streamlit.app/)

[Data source]: (https://kenya.opendataforafrica.org/wcbabvf/immunization-data-for-kenya-2022)

---

### Project Features

- Interactive map of national coverage by immunization indicator
- Bar chart of all indicators for a selected county
- KPI cards showing national average, best, and worst counties
- Top 10 and Bottom 10 performing counties per indicator
- Radar chart summarizing county immunization profile
- Built with **Streamlit**, **Plotly**, and **GeoPandas**

---

###  Goal

Supports Sustainable Development Goal 3: Good Health and Well-being

This dashboard contributes to SDG 3.2 — "End preventable deaths of newborns and children under 5 years of age" — by:

- Promoting data-driven decisions for health planners and policymakers.

- Visualizing disparities in immunization coverage across counties to identify underserved regions.

- Monitoring progress over time through historical trends and performance indicators.

- Encouraging public health accountability through transparent and accessible data.

By making this information accessible and actionable, the dashboard helps to ensure no region is left behind in the fight against vaccine-preventable diseases.

---

###  Run Locally

```bash
# Clone the repository
git clone https://github.com/samwanyua/kenya-immunization-dashboard.git
cd kenya-immunization-dashboard
```

### Install dependencies
```
pip install -r requirements.txt
```

### Launch Streamlit app
```
streamlit run streamlit_app.py
```