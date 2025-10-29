# React Code Lookup UI

This project is a React application that provides a user interface for the existing Python code lookup functionality. It allows users to input various parameters and interact with the backend to retrieve information based on the provided data.

## Project Structure

```
react-code-lookup-ui
├── public
│   └── index.html          # Main HTML file for the React application
├── src
│   ├── App.tsx            # Main component that sets up routing and layout
│   ├── components
│   │   └── LookupForm.tsx  # User interface for inputting values and handling form submission
│   ├── utils
│   │   └── dateUtils.ts    # Utility functions for date manipulation
│   └── types
│       └── index.ts        # TypeScript interfaces and types
├── package.json            # npm configuration file
├── tsconfig.json           # TypeScript configuration file
└── README.md               # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd react-code-lookup-ui
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the application:**
   ```bash
   npm start
   ```

4. **Open your browser:**
   Navigate to `http://localhost:3000` to view the application.

## Usage

- The application provides a form where users can input values for A2, B2, C2, D2, E2, and F2.
- Upon submission, the form will interact with the Python backend to perform the lookup functionality based on the provided inputs.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.