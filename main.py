from classes.docusign_class import Docusign

if __name__ == "__main__":
    for i in range(25):
        print(f"Test case: {i+1}")
        docusign = Docusign("https://app.docusign.com/")
        docusign.login("cahoxom913@nitynote.com","cahoxom913@nitynote.com")
        docusign.load_templates_page()
        docusign.open_template_edit_page("test template")
        print("End of test case\n")






    # for i in range(1):
    #     docusign.open_template_edit_page("test template")
    #     # docusign.edit_template()
    #     # docusign.use_template("test name","cahoxom913@nitynote.com")
    #     # docusign.load_templates_page()
    #     # print(i)
