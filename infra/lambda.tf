resource "aws_lambda_function" "demo_api_posts" {
  function_name = "demo-api-posts"
  runtime       = "python3.11"
  handler       = "lambda_function.lambda_handler"
  timeout       = 30
  memory_size  = 128

  filename         = "../lambda_package/lambda_upload.zip"
source_code_hash = filebase64sha256("../lambda_package/lambda_upload.zip")

  role = aws_iam_role.lambda_exec.arn
}
