from invoke import task


@task
def compile(ctx, service_name, service):
    srv_path = f"{service_name}/"
    cmd = f"python -m grpc_tools.protoc -Iprotos/ --python_out={srv_path} " \
          f"--grpc_python_out={srv_path} protos/{service}.proto"
    ctx.run(cmd)


@task
def compile_all(ctx):
    compile(ctx, "discount_service", "discounter")
    compile(ctx, "discount_service", "messages")
    compile(ctx, "products_service", "products")
    compile(ctx, "products_service", "messages")
    compile(ctx, "users_service", "users")
    compile(ctx, "users_service", "messages")
    compile(ctx, "rest_api", "users")
    compile(ctx, "rest_api", "products")
    compile(ctx, "rest_api", "messages")
