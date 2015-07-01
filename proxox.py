import argparse
import os
from subprocess import call




"""
Check if all the necessary permissions are granted to the user and if all
applications are available in the environment as well as the necessary tools
like sed
"""
def checkenvironment(args):
    # check if file is available / exception
    #[TODO] finish check
    if (os.path.isfile(str(os.getcwd()) + args.config)):
        print("Config file " + args.config + " does not exist")
        return False
    else:
        return True

    # todo check basic tools (sed ...)



    # todo check applications / are these apps callable



    # todo check privileges (config files / open, write) / is the script executed with root permissions / sudo?
    # make sure that if there is a call which requires root permissions - an exception will be thrown


    # todo make tools available for terminal command injection
    # ask for path for command injection


    # todo proxox conf file
    # std. profil / rc file for sourcing
    # std. path to ttyecho binary
    # std. path to runas





def getconfig(cfgpath):
    #cfglist = []
    cfgfile = open(cfgpath, 'r')
    for line in cfgfile:
        if not line.startswith('#') and line.rstrip() != '':
            #cfglist.append(line.rstrip().split(','))
            yield line.rstrip().split(',')
    #yield cfglist



def applytoapp(*funcargs):
    # arguments for applications are in the following order:
    # 0. SET/UNSET, 1. PROXY, 3. APPLICATION SET CALL, 4. APPLICATION UNSET CALL

    if funcargs[0] == 'set':
        callstmt = funcargs[3] + " " + funcargs[1]
        #call(callstmt, shell=True)
    else:
        callstmt = funcargs[4]
        #call(callstmt, shell=True)

    print callstmt
    #return call(callstmt)



def applytoenv(*funcargs):
    #print funcargs[2]
    # arguments for environment variables are in the following order:
    # 0. SET/UNSET, 1. PROXY, 3. VARIABLE, ENVFILE
    envfile = '/etc/profile'

    if funcargs[0] == 'set':

        # check for excepitons defined in the file like local exception rules
        #funcargs[4] != null
        #[TODO] exceptions for version two

        exportstmt = "sed -i.bak '\$aexport " + funcargs[3] + '=' + funcargs[1] + "' " + envfile

        #print callstmt.split()
        #TODO add export stmt to environment file
        #call(callstmt, shell=True)

        #TODO inject source command to all active terminals - source environment file



        #TODO inject command to delete last entrie from history
    else:
        exportstmt = "sed -i.bak '/" + funcargs[3] + " /d' " + envfile
        #call(callstmt, shell=True)

    print exportstmt
    #return call(callstmt)



def applytocfg(*funcargs):
    # 0. SET/UNSET, 1. PROXY, 3. CONFIG_FILE_NAME, 4. CONFIG_VARIABLE, 5. SET_PARAMETER, 6. UNSET_PARAMETER

    if funcargs[0] == 'set':
        callstmt = "sed -i.bak 's/^" + funcargs[4] + "=.*/" + funcargs[4] + "=" + funcargs[5] + "/' " + "'" + funcargs[3] + "'"
        #call(callstmt, shell=True)
    else:
        callstmt = "sed -i.bak 's/^" + funcargs[4] + "=.*/" + funcargs[4] + "=" + funcargs[6] + "/' " + "'" + funcargs[3] + "'"
        #call(callstmt, shell=True)

    print callstmt
    #return call(callstmt)


def applytosystem(*funcargs):
    # 0. SET/UNSET, 1. PROXY, 3. INTERFACE


    if funcargs[0] == 'set':
        # http proxy
        proxy_type = 'webproxy '
        callstmt_param = "sudo networksetup -set" + proxy_type + funcargs[3] + ' ' + getcomponents(funcargs[1])[0] + getcomponents(funcargs[1])[1]
        callstmt_on = "sudo networksetup -set" + proxy_type + funcargs[1] + " " + " on"
        #call(callstmt_param, shell=True)
        #call(callstmt_on, shell=True)
        print callstmt_param
        print callstmt_on

        # https proxy
        proxy_type= 'securewebproxy '
        callstmt_param = "sudo networksetup -set" + proxy_type + funcargs[3] + ' ' + getcomponents(funcargs[1])[0] + getcomponents(funcargs[1])[1]
        callstmt_on = "sudo networksetup -set" + proxy_type + funcargs[1] + " " + " on"
        #call(callstmt_param, shell=True)
        #call(callstmt_on, shell=True)
        print callstmt_param
        print callstmt_on

    else:
        proxy_type = 'webproxystate '
        callstmt_off = "sudo networksetup -set" + proxy_type  + funcargs[3] + " " + " off"
        #call(callstmt_off, shell=True)
        print callstmt_off

        proxy_type = 'securewebproxystate '
        callstmt_off = "sudo networksetup -set" + proxy_type  + funcargs[3] + " " + " off"
        #call(callstmt_off, shell=True)

        print callstmt_off

    return False


""" Return responsible function """
def parsecfgid(cfgid):
    cfgitems = {0: applytosystem,
                1: applytoenv,
                2: applytocfg,
                3: applytoapp
    }
    return cfgitems[cfgid]



""" Return specific proxy prefix """
def getprefix(command):
    if 'https' in command:
        return 'https://'
    else:
        return 'http://'


""" Return single proxy components, host and port """
def getcomponents(proxy):
    return proxy.split(':')

#def applyproxy():
    # if set / unset
    # proxy config already set


def getargparser():
    parser = argparse.ArgumentParser(description="Configure proxy settings for all specified applications")
    parser.add_argument('proxy', help='the proxy host to set up: PROXY:PORT')
    parser.add_argument('--config', default='proxox.cfg',
                        help='the path to the config file, by default its proxox.cfg in the working dir')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--set', help='set proxy configuration', action="store_true")
    group.add_argument('--unset', help='unset proxy configuration', action="store_true")
    parser.add_argument_group(group)
    parser.add_argument('--check',
                        help='checks if application, user is allowed to apply proxy changes in all listed' \
                             ' applications and if no config file is locked due to a still running application',
                        action="store_true")
    parser.add_argument('--verbose', help='enables verbose logging to stdout', action="store_true")

    return parser


if __name__ == "__main__":
    # get a customized arg parser
    parser = getargparser()
    args = parser.parse_args()



    #if not(args.check == True & checkenvironment(args)):
    #    exit()


    # load config file
    cfglist = getconfig(args.config)



    if(args.set == True):
        command = "set"
    else:
        command = "unset"

    for cfg in cfglist:

        funcargs = (command, getprefix(cfg[1]) + args.proxy) + tuple(cfg)
        #print funcargs
        #[TODO] get rid of duplicates - creating a hash over each line and deliting the same hash
        parsecfgid(int(cfg[0]))(*funcargs)
