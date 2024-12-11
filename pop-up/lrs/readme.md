# Route and Measures Information Viewer

This repository contains an HTML template designed to display structured information about routes, measures, and their associated attributes. The layout is clean, readable, and organized into three distinct sections: **Measures**, **Route**, and **Attributes**.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Structure](#structure)
- [Usage](#usage)

## Overview
The template is built to display route and measure details in a tabular format for web-based applications. It includes proper alignment and styling to ensure clarity and a user-friendly experience.

## Features
- **Three organized sections:**  
  - **Measures**: Displays distance-related data, including start, end, and length.
  - **Route**: Contains route-specific identifiers and dates.
  - **Attributes**: Provides additional metadata about the route.
- **Responsive layout:** Uses CSS flexbox for aligned headings.
- **Readable tables:** Proper padding and alignment for tabular data.
- **Dynamic placeholders:** Includes placeholders (`{...}`) to be populated programmatically.

## Structure
### 1. **Measures Section**
Displays details such as:
- Total Measure
- Cartographic Measure
- Start and End Points
- Overall Length
- Units (Miles - US Survey)

### 2. **Route Section**
Includes route-specific details like:
- Route ID
- Datum ID
- Line Order
- Date Range (From Date and To Date)

### 3. **Attributes Section**
Provides metadata for the route:
- Object IDs
- Route Prefix, Number, Suffix, and Section
- Government Level and Route Type
- County, Owner Date, and District

## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/route-measures-viewer.git
