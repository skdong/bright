import auth

url = 'http://console.oceanstack.slancer.com/os/network/v2.0/security-groups'


def test():
    print auth.get_auth_session().get(url).json()


def main():
    test()


if __name__ == '__main__':
    main()
