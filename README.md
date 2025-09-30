# Stepwise Data Analysis Service

This service performs stepwise data analysis on uploaded datasets. It allows flexible processing pipelines by implementing the Chain of Responsibility design pattern.

## Features

- Upload datasets for analysis (e.g., CSV files)
- Perform various analysis steps (e.g., cleaning, transformation, visualization)
- Configure custom processing pipelines
- Each processing step is handled by a separate component in the chain
- Easily extend or modify the analysis workflow (SOLID principles applied) 

## Design Pattern

The service uses the **Chain of Responsibility** pattern to enable flexible and modular data processing. Each handler in the chain performs a specific analysis step and passes the dataset to the next handler.

## Usage

1. Upload your dataset.
2. Define the sequence of analysis steps.
3. Run the pipeline to process your data.

## Extending

To add new analysis steps, implement a new handler and add it to the chain.

## License

MIT