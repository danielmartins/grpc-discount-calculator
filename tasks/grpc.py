from invoke import task


@task
def compile(ctx, service_name):
    srv_path = f"{service_name}/{service_name}"
    cmd = f"python -m grpc_tools.protoc -Iprotos/ --python_out={srv_path} --grpc_python_out={srv_path} protos/discount.proto"
    ctx.run(cmd)
