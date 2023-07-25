import unittest
import os
import json
from create_dataset import should_skip_pdf_file, generate_question_answers
from create_dataset import process_pdf_files

class TestCreateDataset(unittest.TestCase):

    def setUp(self):
        self.test_pdf_file = "test.pdf"
        self.test_output_folder = "./test_output"
        self.test_page_text = "This is a test page."
        self.test_current_page = 0
        os.makedirs(self.test_output_folder, exist_ok=True)

    def tearDown(self):
        # Remove the test output folder and files
        for file_name in os.listdir(self.test_output_folder):
            file_path = os.path.join(self.test_output_folder, file_name)
            os.remove(file_path)
        os.rmdir(self.test_output_folder)

    def test_should_skip_pdf_file(self):
        # Test that should_skip_pdf_file returns an empty list and 0 when there are no existing JSON files
        json_files, last_page_number = should_skip_pdf_file(self.test_pdf_file, self.test_output_folder)
        self.assertEqual(json_files, [])
        self.assertEqual(last_page_number, 0)

        # Test that should_skip_pdf_file returns the correct list of JSON files and last page number when there are existing JSON files
        # Create a test JSON file
        test_json_file = f"{os.path.splitext(self.test_pdf_file)[0]}_page_0_qa.json"
        test_json_file_path = os.path.join(self.test_output_folder, test_json_file)
        with open(test_json_file_path, 'w') as test_json_file:
            test_json_file.write("[\n]\n")
        # Call should_skip_pdf_file
        json_files, last_page_number = should_skip_pdf_file(self.test_pdf_file, self.test_output_folder)
        self.assertEqual([os.path.basename(f) for f in json_files], [os.path.basename(test_json_file_path)])
        self.assertEqual(last_page_number, 0)
        #
    def test_generate_question_answers(self):
        # Test that generate_question_answers returns a dictionary with questions and answers
        qa_dict = generate_question_answers(self.test_pdf_file, self.test_page_text, self.test_current_page)
        self.assertIsInstance(qa_dict, dict)
        self.assertIn('questions', qa_dict)
        self.assertIn('answers', qa_dict)
        self.assertIsInstance(qa_dict['questions'], list)
        self.assertIsInstance(qa_dict['answers'], list)

def test_process_pdf_files(self):
    # Test that process_pdf_files generates the correct JSON files
    # Create a test PDF file
    test_pdf_file_path = os.path.join(self.test_output_folder, self.test_pdf_file)
    with open(test_pdf_file_path, 'w') as test_pdf_file:
        test_pdf_file.write("This is a test PDF file.")
    # Call process_pdf_files
    process_pdf_files()
    # Check that the correct JSON file was generated
    test_json_file = f"{os.path.splitext(self.test_pdf_file)[0]}_page_0_qa.json"
    test_json_file_path = os.path.join(self.test_output_folder, test_json_file)
    self.assertTrue(os.path.exists(test_json_file_path))
    with open(test_json_file_path, 'r') as test_json_file:
        qa_list = json.load(test_json_file)
        self.assertIsInstance(qa_list, list)
        self.assertEqual(len(qa_list), 0)
    # Remove the test PDF file
    os.remove(test_pdf_file_path)
    
if __name__ == '__main__':
    unittest.main()