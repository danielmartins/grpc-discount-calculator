from invoke import task


@task
def compile(ctx, service_name, service):
    srv_path = f"{service_name}/"
    cmd = f"python -m grpc_tools.protoc -Iprotos/ --python_out={srv_path} " \
          f"--grpc_python_out={srv_path} protos/{service}.proto"
    ctx.run(cmd)


@task
def compile_all(ctx):
    compile(ctx, "products_service/app", "products")
    compile(ctx, "products_service/app", "messages")
    compile(ctx, "users_service/app", "users")
    compile(ctx, "users_service/app", "messages")
    compile(ctx, "rest_api/app", "discounter")
    compile(ctx, "rest_api/app", "users")
    compile(ctx, "rest_api/app", "products")
    compile(ctx, "rest_api/app", "messages")
    compile(ctx, "discount_service/app", "discounter")
    compile(ctx, "discount_service/app", "users")
    compile(ctx, "discount_service/app", "products")
    compile(ctx, "discount_service/app", "messages")
