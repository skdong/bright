import auth

bill_url = 'http://console.ghyun.com.cn/us/bill/'


def syc_project(project_id):
    print auth.get_auth_session().get(bill_url + 'v2/admin_projects/' + project_id + '/sync_info').json()


def repair_project():
    project_id = '49754771f1b049939240ea354188f286'
    syc_project(project_id)


def syc_user(user_id):
    import pdb; pdb.set_trace()
    print auth.get_auth_session().get(bill_url + 'v2/users/' + user_id + '/sync_info').json()


def repair_user():
    user_id = 'd7e63535e994436495bfb46ac363c381'
    syc_user(user_id)


def main():
    # repair_project()
    repair_user()


if __name__ == '__main__':
    main()
