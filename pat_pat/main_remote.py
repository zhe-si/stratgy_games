from pat_pat.user.remote_user import SendUserProxy, ReceiveUserProxy
from pat_pat.user.test_user import TestUser


def main():
    s_p = SendUserProxy(TestUser(), "localhost", ReceiveUserProxy.BIND_PORT)
    s_p.run()


if __name__ == '__main__':
    main()
