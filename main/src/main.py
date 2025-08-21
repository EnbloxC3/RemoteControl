try:
    import gconsole as gcs
    gcs.Console.style_print("RemoteControl server is starting...", "green")
    try:
        import os
        import sys
        import server
        gcs.Console.clear()
        if __name__ == "__main__":
            server.app.run(host=server.HOST, port=server.PORT, debug=server.DEBUG)
        else:
            gcs.Console.style_print("Server is running in a non-main context, starting server...", "yellow")
            server.app.run(host=server.HOST, port=server.PORT, debug=server.DEBUG)
    except Exception as e:
        gcs.Console.style_print(f"Server Start Error: {e}", "red")
        input("Press Any Key to exit...")
except Exception as e:
    print(f"Error: {e}") 