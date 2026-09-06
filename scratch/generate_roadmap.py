import json
from pathlib import Path

def generate_full_roadmap():
    days = []

    # Days 1-30: Python Fundamentals (category: python)
    python_topics = [
        "Python Variables & Data Types", "Functions & Scope", "Lists, Tuples & Sets",
        "Dictionaries & Methods", "List & Dict Comprehensions", "Exception Handling & Custom Errors",
        "File I/O & Context Managers", "OOP: Classes & Objects", "OOP: Inheritance & Polymorphism",
        "OOP: Encapsulation & Properties", "Decorators & Higher-Order Functions", "Generators & Iterators",
        "Lambda Functions & Functional Constructs", "Modules & Package Structure", "Type Hinting & Typing Module",
        "Dataclasses & Structured Data", "String Formatting & Regex Basics", "Date, Time & Timezones",
        "JSON Parsing & Serialization", "CSV & Text Parsing", "Multithreading Basics",
        "Multiprocessing Basics", "Asyncio & Async/Await", "Memory Management & Garbage Collection",
        "Metaclasses & Dunder Methods", "Custom Context Managers", "Shallow vs Deep Copying",
        "Collections, Itertools & Functools", "Logging Architecture & Formatters", "Unit Testing with pytest"
    ]
    for i, t in enumerate(python_topics, start=1):
        days.append({
            "day": i,
            "category": "python",
            "topic": t,
            "difficulty": "Beginner" if i <= 10 else ("Intermediate" if i <= 24 else "Advanced"),
            "title": f"Day {i:03d}: {t}",
            "description": f"Comprehensive exercise and practical implementation of {t}.",
            "learning_objectives": [f"Master core concepts of {t}.", "Write clean, tested Python code."],
            "expected_output": "Python implementation file and pytest test suite."
        })

    # Days 31-60: Advanced Python + DSA (category: dsa / python)
    dsa_topics = [
        "Big-O Time & Space Complexity", "Arrays & Dynamic Matrix Operations", "Two Pointers Technique",
        "Sliding Window Pattern", "Prefix Sum Arrays", "Binary Search & Rotated Array Search",
        "Bubble & Insertion Sort", "Merge Sort (Divide & Conquer)", "Quick Sort & Partitioning",
        "Singly Linked List Operations", "Doubly Linked List & LRU Cache", "Stack Data Structure & Evaluation",
        "Queue & Monotonic Deque", "Binary Tree Traversals", "Binary Search Tree (BST) Operations",
        "Heaps & Priority Queues", "Graph BFS Traversal", "Graph DFS Traversal",
        "Dijkstra's Shortest Path Algorithm", "Topological Sort (Kahn's Algorithm)", "Dynamic Programming: 1D DP",
        "DP: 0/1 Knapsack Problem", "DP: Longest Common Subsequence", "Bit Manipulation Operations",
        "Trie (Prefix Tree)", "Union-Find (Disjoint Set)", "Greedy Interval Scheduling",
        "Backtracking: N-Queens & Permutations", "Substring Search (KMP Algorithm)", "Python Creational Design Patterns"
    ]
    for i, t in enumerate(dsa_topics, start=31):
        cat = "dsa" if i <= 58 else "python"
        days.append({
            "day": i,
            "category": cat,
            "topic": t,
            "difficulty": "Intermediate" if i <= 45 else "Advanced",
            "title": f"Day {i:03d}: {t}",
            "description": f"Algorithmic problem solving and data structure implementation for {t}.",
            "learning_objectives": [f"Understand algorithmic mechanics of {t}.", "Implement unit tests for edge cases."],
            "expected_output": f"Code implementation and pytest test suite in learning/{cat}/"
        })

    # Days 61-90: SQL + Statistics (category: sql / statistics)
    sql_stat_topics = [
        ("SQL DDL: Tables & Constraints", "sql"), ("SQL DML: Insert, Update, Delete", "sql"),
        ("SQL Filtering, Sorting & Limiting", "sql"), ("SQL Aggregations & Group By", "sql"),
        ("SQL Inner, Left, Right & Full Outer Joins", "sql"), ("SQL Subqueries & Correlated Queries", "sql"),
        ("SQL Window Functions: ROW_NUMBER, RANK", "sql"), ("SQL Window Functions: LAG, LEAD, SUM OVER", "sql"),
        ("SQL Common Table Expressions (CTEs)", "sql"), ("SQL Indexing & Query Optimization", "sql"),
        ("SQL Case Statements & Conditional Logic", "sql"), ("SQL Date & String Utilities", "sql"),
        ("SQL Set Operations: UNION, EXCEPT", "sql"), ("SQL Views & Materialized Views", "sql"),
        ("SQL Schema Normalization (1NF to 3NF)", "sql"),
        ("Descriptive Statistics: Mean, Std Dev, Variance", "statistics"),
        ("Probability Distributions: Normal, Binomial, Poisson", "statistics"),
        ("Central Limit Theorem & Sampling", "statistics"),
        ("Confidence Intervals & Estimation", "statistics"),
        ("Hypothesis Testing: Z-Test & One-Sample t-Test", "statistics"),
        ("Hypothesis Testing: Two-Sample t-Test", "statistics"),
        ("Chi-Square Test of Independence", "statistics"),
        ("ANOVA (Analysis of Variance)", "statistics"),
        ("Pearson & Spearman Correlation", "statistics"),
        ("Covariance & Covariance Matrix", "statistics"),
        ("Simple Linear Regression Theory", "statistics"),
        ("Multiple Linear Regression & Multicollinearity", "statistics"),
        ("Logistic Regression Log-Odds & Sigmoid", "statistics"),
        ("Bayes Theorem & Conditional Probability", "statistics"),
        ("A/B Testing & Sample Size Calculation", "statistics")
    ]
    for i, (t, cat) in enumerate(sql_stat_topics, start=61):
        days.append({
            "day": i,
            "category": cat,
            "topic": t,
            "difficulty": "Intermediate" if i <= 80 else "Advanced",
            "title": f"Day {i:03d}: {t}",
            "description": f"Hands-on exercise covering {t}.",
            "learning_objectives": [f"Understand practical application of {t}.", "Write executable verification tests."],
            "expected_output": f"Exercise script and test file in learning/{cat}/"
        })

    # Days 91-120: NumPy + Pandas (category: numpy / pandas)
    np_pd_topics = [
        ("NumPy Array Attributes & Initialization", "numpy"), ("NumPy Slicing & Boolean Masking", "numpy"),
        ("NumPy Vectorized Ufuncs", "numpy"), ("NumPy Broadcasting Mechanics", "numpy"),
        ("NumPy Linear Algebra & Matrix Dot Product", "numpy"), ("NumPy Random Sampling & Seeds", "numpy"),
        ("NumPy Axis-wise Aggregations", "numpy"), ("NumPy Reshaping & Stacking", "numpy"),
        ("NumPy Memory Views vs Copies", "numpy"), ("NumPy Benchmarking vs Python Loops", "numpy"),
        ("Pandas Series & DataFrame Setup", "pandas"), ("Pandas Data Summarization & Inspection", "pandas"),
        ("Pandas Indexing: loc, iloc & Filtering", "pandas"), ("Pandas Handling Missing Values", "pandas"),
        ("Pandas Data Type Conversions", "pandas"), ("Pandas GroupBy & Multi-Aggregations", "pandas"),
        ("Pandas Merging & Joining DataFrames", "pandas"), ("Pandas Reshaping: Pivot & Melt", "pandas"),
        ("Pandas String Operations (.str)", "pandas"), ("Pandas Datetime Operations (.dt)", "pandas"),
        ("Pandas Custom Vectorized Apply Functions", "pandas"), ("Pandas Sorting & Ranking", "pandas"),
        ("Pandas Duplicate Removal & Deduplication", "pandas"), ("Pandas Rolling & Expanding Windows", "pandas"),
        ("Pandas MultiIndex Data Operations", "pandas"), ("Pandas Categorical Data Encoding", "pandas"),
        ("Pandas Exponentially Weighted Metrics", "pandas"), ("Pandas Parquet & CSV I/O", "pandas"),
        ("Pandas Method Chaining Pipelines", "pandas"), ("Pandas Memory & Query Optimization", "pandas")
    ]
    for i, (t, cat) in enumerate(np_pd_topics, start=91):
        days.append({
            "day": i,
            "category": cat,
            "topic": t,
            "difficulty": "Beginner" if i <= 100 else ("Intermediate" if i <= 115 else "Advanced"),
            "title": f"Day {i:03d}: {t}",
            "description": f"Data processing implementation focused on {t}.",
            "learning_objectives": [f"Master data manipulation using {t}.", "Verify data transformation outputs."],
            "expected_output": f"Python data script and test file in learning/{cat}/"
        })

    # Days 121-160: Data Analysis + Data Visualization (category: data-analysis)
    da_topics = [
        "Exploratory Data Analysis Workflow", "Outlier Detection via IQR & Z-Score",
        "Feature Scaling: Standard vs MinMax", "Handling Imbalanced Datasets via Resampling",
        "Multicollinearity & VIF Analysis", "Automated Data Profiling",
        "Data Wrangling & Cleaning Pipeline", "Cohort Analysis & Retention Curves",
        "RFM Customer Segmentation", "Multi-Step Funnel Conversion Metrics",
        "Distribution Skewness & Transformations", "Business Metric Aggregations",
        "Feature Engineering: Binning & Polynomials", "Text Feature Extraction for Tabular Data",
        "KNN & Multivariate Imputation", "Time Series Trend-Seasonality Decomposition",
        "Data Quality Schema Validation", "Geospatial Lat/Long Distance Calculations",
        "Statistical Lift & Significance in EDA", "End-to-End EDA Case Study",
        "Matplotlib Figure & Axes Architecture", "Line Plots for Time Series",
        "Grouped & Stacked Bar Charts", "Histograms & KDE Density Overlays",
        "Scatter Plots & Feature Correlations", "Box Plots & Distribution Comparisons",
        "Annotated Heatmaps", "Custom Color Palettes & Accessible Styling",
        "Multi-panel Subplot Grids", "Interactive Plotting Specs",
        "Error Bars & Confidence Bands", "Pairwise Scatter Matrix Visuals",
        "Geospatial Map Plots", "Financial Candlestick Charts",
        "ROC Curves & Precision-Recall Plots", "Chart Annotations & Visual Storytelling",
        "High-DPI Figure Exporting", "Executive Dashboard Layout Rules",
        "3D Surface & Mesh Plots", "Executive Data Storytelling Summary"
    ]
    for i, t in enumerate(da_topics, start=121):
        days.append({
            "day": i,
            "category": "data-analysis",
            "topic": t,
            "difficulty": "Intermediate" if i <= 145 else "Advanced",
            "title": f"Day {i:03d}: {t}",
            "description": f"Analytical problem solving and visual insights for {t}.",
            "learning_objectives": [f"Implement analytical workflow for {t}.", "Validate metrics via tests."],
            "expected_output": "Data analysis script, visualization specs, and pytest file in learning/data-analysis/"
        })

    # Days 161-220: Machine Learning (category: machine-learning)
    ml_topics = [
        "ML Problem Formulation & Framing", "Linear Regression from Scratch", "Gradient Descent (Batch, SGD, Mini-batch)",
        "Ridge Regularization (L2)", "Lasso Regularization (L1)", "ElasticNet Regularization",
        "Logistic Regression from Scratch", "Multiclass Classification (OvR)", "Regression Metrics (MSE, RMSE, R2)",
        "Classification Metrics (Accuracy, Precision, Recall, F1)", "ROC Curve & ROC-AUC Metric", "Precision-Recall Curve Analysis",
        "k-Nearest Neighbors (k-NN)", "Decision Tree Classifier from Scratch", "Decision Tree Regressor & Pruning",
        "Random Forest Classifier & Bagging", "Feature Importance (MDI vs Permutation)", "AdaBoost Classifier",
        "Gradient Boosting Machines (GBM)", "XGBoost Regularized Boosting", "LightGBM Leaf-wise Tree Growth",
        "CatBoost Categorical Processing", "Linear Support Vector Machines", "SVM Kernel Trick (RBF Kernel)",
        "Gaussian Naive Bayes", "Grid Search & Random Search", "Bayesian Hyperparameter Optimization",
        "Stratified & TimeSeries Cross-Validation", "Bias-Variance Tradeoff Analysis", "Learning Curves & Overfitting Diagnosis",
        "Principal Component Analysis (PCA)", "Truncated SVD Dimensionality Reduction", "t-SNE Manifold Visualization",
        "UMAP Dimensionality Reduction", "k-Means Clustering from Scratch", "Elbow Method & Silhouette Score",
        "Hierarchical Agglomerative Clustering", "DBSCAN Spatial Clustering", "Gaussian Mixture Models (GMM)",
        "Isolation Forest Anomaly Detection", "One-Class SVM Novelty Detection", "Time Series AutoRegression (AR)",
        "Time Series Moving Average (MA)", "ARIMA & SARIMA Modeling", "Exponential Smoothing (Holt-Winters)",
        "User-Based Collaborative Filtering", "Item-Based Collaborative Filtering", "SVD Matrix Factorization",
        "Semi-Supervised Self-Training", "Ensemble Stacking & Blending", "Feature Selection (RFE & SelectKBest)",
        "Cost-Sensitive Imbalanced Learning", "Probability Calibration (Platt Scaling)", "Out-of-Fold Target Encoding",
        "Data Leakage Audit & Prevention", "SHAP Feature Explanations", "LIME Local Model Interpretability",
        "Model Serialization (Joblib & ONNX)", "Scikit-Learn Pipeline Construction", "Automated ML Benchmark Suite"
    ]
    for i, t in enumerate(ml_topics, start=161):
        days.append({
            "day": i,
            "category": "machine-learning",
            "topic": t,
            "difficulty": "Intermediate" if i <= 190 else "Advanced",
            "title": f"Day {i:03d}: {t}",
            "description": f"Supervised/Unsupervised machine learning module for {t}.",
            "learning_objectives": [f"Understand theoretical & practical framework of {t}.", "Evaluate model outputs with tests."],
            "expected_output": "Machine learning code, evaluation logic, and unit test file in learning/machine-learning/"
        })

    # Days 221-250: Advanced Machine Learning & Deep Learning Foundation (categories: machine-learning / deep-learning)
    adv_ml_topics = [
        ("Quantile Regression", "machine-learning"), ("Multi-Label Classification", "machine-learning"),
        ("Spatial-Temporal Feature Engineering", "machine-learning"), ("Graph Machine Learning Node Embeddings", "machine-learning"),
        ("Kaplan-Meier Survival Analysis", "machine-learning"), ("Cox Proportional Hazards Model", "machine-learning"),
        ("Propensity Score Matching", "machine-learning"), ("Difference-in-Differences Causal Inference", "machine-learning"),
        ("Genetic Algorithms for Optimization", "machine-learning"), ("Particle Swarm Optimization", "machine-learning"),
        ("Conformal Prediction Intervals", "machine-learning"), ("Active Learning Uncertainty Sampling", "machine-learning"),
        ("Streaming Online Machine Learning", "machine-learning"), ("Multi-Armed Bandits (Epsilon-Greedy)", "machine-learning"),
        ("Contextual Bandits Framework", "machine-learning"),
        ("Artificial Neural Network Perceptron", "deep-learning"), ("Multi-Layer Perceptron (MLP) from Scratch", "deep-learning"),
        ("Activation Functions (ReLU, Sigmoid, Tanh, GELU)", "deep-learning"), ("Forward & Backward Propagation", "deep-learning"),
        ("Loss Functions (Cross-Entropy, MSE, Focal Loss)", "deep-learning"), ("Gradient Vanishing & Explosion Remedies", "deep-learning"),
        ("Optimizers: SGD, Momentum, RMSprop, Adam", "deep-learning"), ("Learning Rate Schedulers (Cosine Annealing)", "deep-learning"),
        ("Batch Normalization & Layer Normalization", "deep-learning"), ("Dropout & Regularization in NNs", "deep-learning"),
        ("Weight Initialization Strategies (Xavier, He)", "deep-learning"), ("PyTorch Tensors & Autograd Engine", "deep-learning"),
        ("PyTorch nn.Module & Custom Training Loop", "deep-learning"), ("PyTorch Dataset & DataLoader", "deep-learning"),
        ("Early Stopping & Model Checkpointing", "deep-learning")
    ]
    for i, (t, cat) in enumerate(adv_ml_topics, start=221):
        days.append({
            "day": i,
            "category": cat,
            "topic": t,
            "difficulty": "Advanced",
            "title": f"Day {i:03d}: {t}",
            "description": f"Advanced machine learning/deep learning implementation of {t}.",
            "learning_objectives": [f"Master mathematical & computational principles of {t}.", "Implement tests verifying accuracy."],
            "expected_output": f"Code module and test file in learning/{cat}/"
        })

    # Days 251-280: Deep Learning Architecture (category: deep-learning)
    dl_topics = [
        "Convolutional Neural Networks (CNN) Basics", "CNN Pooling & Stride Operations",
        "ResNet Architecture & Residual Connections", "Data Augmentation for Image Tensors",
        "Transfer Learning & Fine-tuning CNNs", "Recurrent Neural Networks (RNN) Mechanics",
        "Long Short-Term Memory (LSTM) Networks", "Gated Recurrent Units (GRU)",
        "Bidirectional RNNs & LSTMs", "Sequence-to-Sequence Architecture & Attention",
        "Self-Attention Mechanism Math", "Multi-Head Attention from Scratch",
        "Positional Encoding in Transformers", "Transformer Encoder Block Architecture",
        "Transformer Decoder Block Architecture", "Autoencoders for Anomaly Detection",
        "Variational Autoencoders (VAE) Latent Space", "Generative Adversarial Networks (GAN) Basics",
        "Deep Q-Networks (DQN) Reinforcement Learning", "Policy Gradient Methods (REINFORCE)",
        "Proximal Policy Optimization (PPO) Concepts", "Graph Neural Networks (GCN Layer)",
        "Model Quantization & FP16 Mixed Precision", "Neural Network Pruning Techniques",
        "Knowledge Distillation Teacher-Student", "Contrastive Learning (SimCLR Loss)",
        "SIAM Networks & Triplet Loss", "Object Detection (YOLO Principles)",
        "Semantic Segmentation (U-Net Architecture)", "Deep Learning Model Inference Optimization"
    ]
    for i, t in enumerate(dl_topics, start=251):
        days.append({
            "day": i,
            "category": "deep-learning",
            "topic": t,
            "difficulty": "Advanced",
            "title": f"Day {i:03d}: {t}",
            "description": f"Deep learning neural network implementation covering {t}.",
            "learning_objectives": [f"Understand deep neural mechanics of {t}.", "Verify tensor shapes and operations."],
            "expected_output": "Deep learning code and test file in learning/deep-learning/"
        })

    # Days 281-300: Generative AI & LLMs (category: generative-ai)
    genai_topics = [
        "LLM Architecture Overview & Tokenization", "BPE & WordPiece Tokenizer Implementation",
        "Prompt Engineering Strategies & Few-Shot", "Chain-of-Thought (CoT) Prompting",
        "Structured Output Parsing & JSON Schemas", "LLM API Integration & Rate Handling",
        "Embeddings Generation & Cosine Distance", "Vector Store Indexing & Similarity Search",
        "Retrieval-Augment Generation (RAG) Pipeline", "Document Chunking & Overlap Strategies",
        "Hybrid Search (Dense + Sparse BM25)", "Re-ranking Search Results using Cross-Encoders",
        "Agentic Workflows & Tool Calling", "ReAct Agent Pattern Implementation",
        "Memory Management in Conversational AI", "Fine-Tuning LLMs (PEFT & LoRA Concepts)",
        "Quantization (GGUF, AWQ, 4-bit/8-bit)", "LLM Evaluation Metrics (ROUGE, BLEU, G-Eval)",
        "Guardrails & Safety Input/Output Filtering", "Local LLM Serving & Inference Engines"
    ]
    for i, t in enumerate(genai_topics, start=281):
        days.append({
            "day": i,
            "category": "generative-ai",
            "topic": t,
            "difficulty": "Advanced",
            "title": f"Day {i:03d}: {t}",
            "description": f"Generative AI engineering task covering {t}.",
            "learning_objectives": [f"Implement production LLM pattern for {t}.", "Write test assertions verifying output."],
            "expected_output": "Generative AI Python module and test suite in learning/generative-ai/"
        })

    # Days 301-320: Web Development & APIs (categories: web-development / apis)
    web_api_topics = [
        ("HTTP Protocol Fundamentals & Verbs", "web-development"), ("HTML5 & CSS3 Structure for Data Portals", "web-development"),
        ("JavaScript ES6 Basics for Data Dashboards", "web-development"), ("REST API Architectural Principles", "apis"),
        ("Building REST APIs with Python (http.server / Lightweight)", "apis"), ("Request Routing & Query Parameters", "apis"),
        ("JSON Response Payloads & Error Codes", "apis"), ("API Request Validation & Schemas", "apis"),
        ("API Authentication: API Keys & Headers", "apis"), ("API Authentication: JWT Tokens", "apis"),
        ("API Rate Limiting & Throttling Logic", "apis"), ("FastAPI Framework Fundamentals", "apis"),
        ("FastAPI Pydantic Request Models", "apis"), ("FastAPI Dependency Injection System", "apis"),
        ("FastAPI Async Route Handlers", "apis"), ("Swagger UI & OpenAPI Specification", "apis"),
        ("Webhooks & Event-Driven API Callbacks", "apis"), ("WebSocket Real-Time Data Streaming", "web-development"),
        ("CORS (Cross-Origin Resource Sharing)", "web-development"), ("Full-Stack Data Web App Architecture", "web-development")
    ]
    for i, (t, cat) in enumerate(web_api_topics, start=301):
        days.append({
            "day": i,
            "category": cat,
            "topic": t,
            "difficulty": "Intermediate" if i <= 310 else "Advanced",
            "title": f"Day {i:03d}: {t}",
            "description": f"Web & API development exercise covering {t}.",
            "learning_objectives": [f"Build functional web/API component for {t}.", "Test endpoint behavior with unit tests."],
            "expected_output": f"Web/API code and test file in learning/{cat}/"
        })

    # Days 321-340: Docker, Git & Deployment (categories: docker / git-github)
    devops_topics = [
        ("Git Version Control Fundamentals", "git-github"), ("Git Branching & Merging Strategies", "git-github"),
        ("Git Interactive Rebase & Commit Cleanups", "git-github"), ("GitHub Actions CI/CD Workflow Basics", "git-github"),
        ("GitHub Actions Secrets & Matrix Builds", "git-github"), ("Docker Concepts: Images, Containers & Registries", "docker"),
        ("Writing Efficient Dockerfiles for Python", "docker"), ("Docker Multi-Stage Builds for Minimal Size", "docker"),
        ("Docker Bind Mounts & Volumes", "docker"), ("Docker Container Networking", "docker"),
        ("Docker Compose Multi-Container Setup", "docker"), ("Containerizing ML Models for Production", "docker"),
        ("Environment Variables & Config Management", "docker"), ("Container Health Checks & Resource Limits", "docker"),
        ("Linting Python Code with Flake8 / Ruff", "git-github"), ("Code Formatting with Black", "git-github"),
        ("Pre-commit Hooks for Security & Quality", "git-github"), ("Automated Semantic Versioning", "git-github"),
        ("Cloud Deployment Principles (Serverless / IaaS)", "docker"), ("Infrastructure as Code Concepts", "docker")
    ]
    for i, (t, cat) in enumerate(devops_topics, start=321):
        days.append({
            "day": i,
            "category": cat,
            "topic": t,
            "difficulty": "Intermediate" if i <= 330 else "Advanced",
            "title": f"Day {i:03d}: {t}",
            "description": f"DevOps and containerization task for {t}.",
            "learning_objectives": [f"Implement container/CI automation for {t}.", "Verify configuration with unit tests."],
            "expected_output": f"Configuration script and test file in learning/{cat}/"
        })

    # Days 341-355: Data Engineering & MLOps (categories: data-engineering / mlops)
    de_mlops_topics = [
        ("ETL Pipeline Architecture Principles", "data-engineering"), ("Data Lake vs Data Warehouse Patterns", "data-engineering"),
        ("Batch Data Ingestion & Validation", "data-engineering"), ("Streaming Data Ingestion Patterns", "data-engineering"),
        ("Parquet & Columnar File Optimization", "data-engineering"), ("Data Partitioning & Indexing", "data-engineering"),
        ("Pipeline DAG Orchestration Concepts", "data-engineering"), ("Schema Evolution & Migration Strategies", "data-engineering"),
        ("MLOps Architecture & Lifecycle Overview", "mlops"), ("MLflow Experiment Tracking & Metrics", "mlops"),
        ("Model Registry & Versioning Workflow", "mlops"), ("Feature Store Design & Online/Offline Stores", "mlops"),
        ("Model Data Drift Detection (KS-Test & PSI)", "mlops"), ("Model Performance Monitoring & Alerting", "mlops"),
        ("Automated Model Retraining Pipelines", "mlops")
    ]
    for i, (t, cat) in enumerate(de_mlops_topics, start=341):
        days.append({
            "day": i,
            "category": cat,
            "topic": t,
            "difficulty": "Advanced",
            "title": f"Day {i:03d}: {t}",
            "description": f"Data engineering and MLOps system task for {t}.",
            "learning_objectives": [f"Build robust data pipeline component for {t}.", "Write verification unit tests."],
            "expected_output": f"Data Engineering / MLOps code module and test in learning/{cat}/"
        })

    # Days 356-365: Portfolio Projects Integration (category: projects)
    project_topics = [
        ("Sales Analysis: Data Ingestion & Cleaning Engine", "projects"),
        ("Sales Analysis: Exploratory Metrics & Aggregations", "projects"),
        ("Sales Analysis: Interactive Visualization Dashboard", "projects"),
        ("Customer Churn: Feature Engineering & Preprocessing", "projects"),
        ("Customer Churn: Model Training & Evaluation Suite", "projects"),
        ("Customer Churn: Model Interpretability & SHAP Insights", "projects"),
        ("ML API: Model Serving Infrastructure", "projects"),
        ("ML API: Request Payload Validation & Middleware", "projects"),
        ("ML Deployment: Dockerized Container Build", "projects"),
        ("365-Day Data Science Journey Capstone Review", "projects")
    ]
    for i, (t, cat) in enumerate(project_topics, start=356):
        days.append({
            "day": i,
            "category": cat,
            "topic": t,
            "difficulty": "Advanced",
            "title": f"Day {i:03d}: {t}",
            "description": f"Portfolio project capstone development step: {t}.",
            "learning_objectives": [f"Integrate production code component for {t}.", "Execute test assertions."],
            "expected_output": "Portfolio project file updates and test suite in projects/"
        })

    out_file = Path("c:/Users/pmshi/OneDrive/Desktop/git_auto/roadmap.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(days, f, indent=2)

    print(f"Generated roadmap.json with {len(days)} items.")

if __name__ == "__main__":
    generate_full_roadmap()
