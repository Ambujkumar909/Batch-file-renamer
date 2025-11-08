📁 Batch File Renamer & Smart Folder Management System
✨ Project Overview
This is an enterprise-grade utility suite built in Python designed to automate and standardize complex file and folder organization tasks at scale. 
The system significantly reduces manual data handling time, enhances regulatory compliance, and establishes consistent digital asset management across large datasets.

The suite comprises two core tools: the Batch File Renamer and the Smart Folder Management System.

🚀 Key Features
1. Batch File Renamer
Custom Pattern Renaming: Allows users to define dynamic patterns for renaming files (e.g., [Date]_[ProjectID]_[Sequence].ext).
Metadata Integration: Ability to extract and insert file metadata (such as creation date, last modified date) directly into the new filename.
Find & Replace: Supports complex text replacement, removal, and case conversion (uppercase, lowercase, title case) on selected file batches.

Preview Mode: Provides a real-time preview of the new filename before any change is committed, ensuring data integrity.

2. Smart Folder Management System
Hierarchical Sorting: Automatically creates and organizes nested folder structures based on rules defined by file attributes (e.g., sort all files into Year/Month/ProjectName directories).

Automated Relocation: Moves and archives files into the new, standardized folder structure post-renaming, streamlining the entire data lifecycle.

Compliance Ready: Ensures all archived data adheres to pre-defined naming and storage conventions for easy auditing.

🛠️ Installation & Setup
Prerequisites
Python 3.7 or higher

pip (Python package installer)

Steps
Clone the Repository:

git clone [Your Repository URL]
cd batch-file-renamer
Install Dependencies:


pip install -r requirements.txt
Run the Utility:

python main.py --help
Note: The primary entry point for the utility is main.py.

💡 Usage Example
To apply a new naming convention of PROJECT-ID-YYYYMMDD_001.pdf to all files in the current directory:

Bash

# Assuming a Command Line Interface (CLI) implementation
python main.py rename --folder ./data --pattern "PO-{location}-%%Y%%m%%d_{seq}" --extension pdf
