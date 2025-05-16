# Document Loader

> Document Loader is a tool to load the document object. LangChain Provide several integration with various data source to load data from: **`Slack`**, **`Notion`**, **`Google Drive`**.

- [Document Loader](#document-loader)
  - [Integration](#integration)
  - [Interface](#interface)

## Integration

- You can find available integration on the document loaders integrations page from [here](https://python.langchain.com/docs/integrations/document_loaders/).

## Interface

- Documents loader implement on the top of [BaseLoader interface](https://python.langchain.com/api_reference/core/document_loaders/langchain_core.document_loaders.base.BaseLoader.html).

- Each document loader has there own specific parameter. But all of them are invoked in the same method **`.load()`** or **`.lazyload()`**.

- **Example**

    ```py
    from langchain_community.document_loaders.csv_loader import CSVLoader
    
    loader = CSVLoader(
        ...  # <-- Integration specific parameters here
    )
    data = loader.load()
    ```

- **When working with large dataset.**

    ```py
    for document in loader.lazy_load():
        print(document)
    ```