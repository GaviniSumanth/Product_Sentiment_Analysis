const urls={};
urls.SUBMIT = "http://127.0.0.1:5000/result/";
urls.FORM =(params) =>"http://127.0.0.1:5000/form?"+ new URLSearchParams(params);
export default urls;