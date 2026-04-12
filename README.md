# Doctor Recommendation ML Portfolio

A portfolio-ready machine learning project for doctor recommendation based on location, specialization, consultation fee, and service filters.

## Project Highlights
- End-to-end ML integration with CatBoost model
- Real dataset-driven recommendations
- Interactive demo interface
- API + UI flow supports input-to-output execution

## Repository Structure

```text
.
├── notebooks/
│   ├── data_exploration.ipynb
│   └── model_testing.ipynb
├── demo_ui/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── models/
│   └── doctor_ai_full_package.pkl
├── data/
│   └── Dr.Seba_500_Organized_Final.xlsx
├── doctor_api.py
├── run_frontend.py
├── requirements.txt
└── README.md
```

## Suggested Metrics Section
Add your real metrics here before publishing:

- Accuracy: `XX.XX%`
- Precision: `XX.XX%`
- Recall: `XX.XX%`
- F1-score: `XX.XX%`

## Run Instructions (Input to Output)

**Django is now the unified backend.** Flask files have been archived to `legacy/`.

### 1) Install dependencies
```bash
pip install -r requirements.txt
```

### 2) Run Django server
```bash
python manage.py runserver
```

### 3) Open in browser
```text
http://127.0.0.1:8000/
```

### 4) Use the application
- Select District, Thana, Specialization, and filter preferences
- Click "🔍 Search Doctors"
- View AI-ranked recommendations by predicted quality score

## Notebook Usage

From VS Code/Jupyter:
- Open `notebooks/data_exploration.ipynb`
- Open `notebooks/model_testing.ipynb`

Both notebooks are aligned to the current folder structure using `models/` and `data/` paths.

## Acknowledgments

### Mentor & Guidance
**Nusrat Jahan** — Data Science Trainer
- Project conceptualization and methodology guidance
- Data science best practices and model selection
- Quality assurance and validation oversight

This project was developed under professional mentorship during an internship program focusing on applied machine learning and data-driven decision systems.

3. Optional co-author commits
Use this when teacher contributes directly:

```text
Co-authored-by: Teacher Name <teacher-email@example.com>
```

## Industry-Level Publishing Checklist
- Keep clear folder boundaries (`notebooks`, `models`, `demo_ui`, `data`)
- Use reproducible run instructions
- Keep model and data versioned intentionally
- Add mentor attribution clearly
- Avoid secrets/credentials in repository

## Notes
- Django v2 is the current production-ready implementation
- Legacy Flask files (`doctor_api.py`, `run_frontend.py`) moved to `legacy/` folder for reference
- See [legacy/README.md](legacy/README.md) for v1 architecture details
- The project follows Django best practices with `drseba_platform` as project and `recommender` as app
