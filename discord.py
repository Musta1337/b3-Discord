# coding=utf-8

__author__ = 'Musta'
__version__ = '1.0'

import b3
import b3.plugin
import b3.events
import datetime
import urllib2
import json
from b3.functions import minutesStr


class DiscordPlugin(b3.plugin.Plugin):

    def __init__(self, console, config=None):
        """
        Build the plugin object.
        :param console: The parser instance.
        :param config: The plugin configuration object instance.
        """
        #########Checking if Admin Plugin is enabled.#########
        b3.plugin.Plugin.__init__(self, console, config)
        self.adminPlugin = self.console.getPlugin('admin')
        if not self.adminPlugin:
            raise AttributeError('could not start without admin plugin')
        ######################################################

    def onLoadConfig(self):
        """
        Load plugin configuration.
        """
        ##Loading data from conf file.##
        self._discordWebhookUrl = self.config.get('data','webhookUrl')
        self._serverName = self.config.get('data','hostname')
        self._b3Version = self.config.get('data','b3Version')
        self._clanName = self.config.get('data','clanName')
        self._clanWebsite = self.config.get ('data','clanWebsite')
        self._clanIcon = self.config.get ('data','clanIcon')
        self._clanBanAppeal = self.config.get ('data','clanBanAppeal')
        #Image below at the plugin startup
        self._clanHeader = self.config.get ('data','clanHeader')
        ################################
    def onStartup(self):
        """
        Initialize plugin settings.
        """

        ########Getting Events from b3 and Assigning to an ID.###########
        self.registerEvent(self.console.getEventID('EVT_CLIENT_BAN'), self.onBan)
        self.registerEvent(self.console.getEventID('EVT_CLIENT_BAN_TEMP'), self.onBan)
        self.registerEvent(self.console.getEventID('EVT_CLIENT_KICK'), self.onKick)
        self.registerEvent(self.console.getEventID('EVT_CLIENT_SAY'), self.onSay)
        self.registerEvent(self.console.getEventID('EVT_CLIENT_CONNECT'), self.onConnect)
        self.registerEvent(self.console.getEventID('EVT_CLIENT_TEAM_SAY'), self.onTeamSay)
        self.registerEvent(self.console.getEventID('EVT_CLIENT_SQUAD_SAY'), self.onSquadSay)
        self.registerEvent(self.console.getEventID('EVT_CLIENT_DISCONNECT'), self.onDisconnect)
        self.registerEvent(self.console.getEventID('EVT_CLIENT_UNBAN'), self.onUnban)
        self.registerEvent(self.console.getEventID('EVT_GAME_MAP_CHANGE'), self.onMapChange)
        ##################################################################

        ##Logging at Plugin Start.##
        self.debug('plugin started')

        ##Pushing Embed message on plugin startup##
        embed = {
            "author": {
                   "name": self._clanName,
                   "icon_url": self._clanIcon
            },
            "title": "Big Brother Bot Discord Integration.",
            "url": self._clanWebsite,
            "description": "Big Brother Bot Discord plugin Succesfully loaded.",
            "timestamp": datetime.datetime.now().isoformat(),
            "color": 65512,
            "image": {
                    "url": self._clanHeader
            },
            "thumbnail": {
                    "url": self._clanIcon
            },
            "fields": [
                {
                    "name": "Connected Server",
                    "value": '%s' % (self._serverName),
                    "inline": True
                },
                {
                    "name": "B3 Version",
                    "value": '%s' % (self._b3Version),
                    "inline": True
                },
                {
                    "name": "Credit",
                    "value": "**Discord Plugin v1.0 by Musta#6735**",
                    "inline": False
                }
            ],
            #"footer": {
            #        "icon_url": self._clanIcon,
            #        "text": self._clanName
            #}
        }	
        #hook = {
        #    "content": 'Plugin started.'
		#}
        #self.discordPush(hook)
        self.discordEmbeddedPush(embed)
    
    def onBan(self, event):
        """
        Perform operations when EVT_CLIENT_BAN or EVT_CLIENT_BAN_TEMP is received.
        :param event: An EVT_CLIENT_BAN or and EVT_CLIENT_BAN_TEMP event.
        """
        ##Getting the even contestants on the line and giving them new name.##
        admin = event.data['admin']
        client = event.client
        reason = event.data['reason']
        ######################################################################
        ##Beautiful Ban message for Beautiful People.##
        embed = {
            "author": {
                   "name": self._clanName,
                   "icon_url": self._clanIcon
            },
            "title": "Client Ban",
            "description": '**%s** Banned **%s**' % (admin.name, client.name),
            "timestamp": datetime.datetime.now().isoformat(),
            "thumbnail": {
                    "url": self._clanIcon
            },
            "color": 16711680,
            "fields": [
                {
                    "name": "Server",
                    "value": self._serverName,
                    "inline": False
                }
            ],
            "footer": {
                    "icon_url": self._clanIcon,
                    "text": self._serverName
            }
        }
        #################################################
        ##AKA If Admin is good who banned##
        if reason:
            embed["fields"].append({
                "name": "Reason for Ban",
                "value": self.console.stripColors(reason),
                "inline": True
            })
        ##RIP Permanent Ban##
        duration = 'permanent'
        if 'duration' in event.data:
        ##This line is little fishy but Got it working.##
            duration = minutesStr(event.data['duration'])
        #################################################
        embed["fields"].append({
                "name": "Duration of Ban",
                "value": duration,
                "inline": True
                })
        ##Pushing message##
        self.discordEmbeddedPush(embed)
    
    def onKick(self, event):
        """Perform operations when EVT_CLIENT_KICK is received.
        :param event: An EVT_CLIENT_KICK event."""
        ##Getting Sub event contestants##
        admin = event.data['admin']
        client = event.client
        reason = event.data['reason']
        #################################
        
        ##Beautiful Kick Message for Beautiful People##
        embed = {
            "author": {
                   "name": self._clanName,
                   "icon_url": self._clanIcon
            },
            "title": "Client kick",
            "description": '**%s** Kicked **%s**' % (admin.name, client.name),
            "timestamp": datetime.datetime.now().isoformat(),
            "thumbnail": {
                    "url": self._clanIcon
            },
            "color": 16728899,
            "fields": [
                {
                    "name": "Server",
                    "value": self._serverName,
                    "inline": False
                }
            ],
            "footer": {
                    "icon_url": self._clanIcon,
                    "text": self._serverName
            }
        }
        ###############################################


        ##AKA If Admin is good who kicked##
        if reason:
            embed["fields"].append({
                "name": "Reason for Kick",
                "value": self.console.stripColors(reason),
                "inline": True
            })
        #pushing message
        self.discordEmbeddedPush(embed)
        
    def onSay(self, event):
        client = event.client
        msg = event.data

        #hook = {
        #    "username": client.name,
        #    "content": '%s' % (msg)
		#}

        hook = {
            "content": '**%s**: %s' % (client.name, msg)
        }
        self.discordPush(hook)

    def onTeamSay(self, event):
        client = event.client
        msg = event.data

        #hook = {
        #    "username": client.name,
        #    "content": '%s' % (msg)
        #}

        hook = {
            "content": '**[Team]%s:** %s' % (client.name, msg)
        }
        self.discordPush(hook)

    def onSquadSay(self, event):
        client = event.client
        msg = event.data

        #hook = {
        #    "username": client.name,
        #    "content": '%s' % (msg)
        #}

        hook = {
            "content": '**%s:** %s' % (client.name, msg)
        }
        self.discordPush(hook)

    def onConnect(self, event):
        client = event.client

        #hook = {
        #    "content": 'Player **%s** Connected to the Server.' % (client.name)
        #}
        #self.discordPush(hook)
        
        embed = {
            "timestamp": datetime.datetime.now().isoformat(),
            "description": "Player **%s** Connected to the server. Client ID: **%s**, Client HWID: **%s**" % (client.name, client.cid, client.guid),
            "color": 2096896
        }
        self.discordEmbeddedPush(embed)

    def onDisconnect(self, event):
        client = event.client
        playerID = event.data

        #hook = {
        #    "content": 'Player **%s** Disconnnected from Server. Player Client ID: **%s**' % (client.name, playerID)
        #}
        #self.discordPush(hook)
        embed = {
            "description": "Player **%s** Disconnected from server." % (client.name),
            "color": 16722432
        }
        self.discordEmbeddedPush(embed)

    def onUnban(self, event):
        client = event.client
        reason = event.reason

        embed = {
            "author": {
                   "name": self._clanName,
                   "icon_url": self._clanIcon
            },
            "title": "Client Unbanned",
            "description": '**%s** has been unbanned from the server.' % (client.name),
            "timestamp": datetime.datetime.now().isoformat(),
            "thumbnail": {
                    "url": self._clanIcon
            },
            "color": 3866368,
            "fields": [
                {
                    "name": "Server",
                    "value": self._serverName,
                    "inline": False
                }
            ],
            "footer": {
                    "icon_url": self._clanIcon,
                    "text": self._serverName
            }
        }


        if reason:
            embed["fields"].append({
                "name": "Reason for Unban",
                "value": self.console.stripColors(reason),
                "inline": True
                })
        
        self.discordEmbeddedPush(embed)
    
    def onMapChange(self, event):
        oldMap = event.data['old']
        newMap = event.data['new']

        embed = {
            #"author": {
            #       "name": self._clanName,
            #       "icon_url": self._clanIcon
            #},
            "description": '**Map has been changed.**',
            "timestamp": datetime.datetime.now().isoformat(),
            #"thumbnail": {
            #        "url": self._clanIcon
            #},
            "color": 3866368,
            "fields": [
                {
                    "name": "Old Map",
                    "value": oldMap,
                    "inline": True
                },
                {
                    "name": "New Map",
                    "value": newMap,
                    "inline": True
                }
            ],
            "footer": {
                    "icon_url": self._clanIcon,
                    "text": self._serverName
            }
        }
        self.discordEmbeddedPush(embed)

    def discordPush(self, hook):
        data = json.dumps(hook)
        req = urllib2.Request(self._discordWebhookUrl, data, {
                'Content-Type': 'application/json',
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36"
        })
        try:
            f = urllib2.urlopen(req)
            response = f.read()
            f.close()
        except urllib2.HTTPError as ex:
            self.debug("Cannot push data to Discord. is your webhook url right?")
            self.debug("Data: %s\nCode: %s\nRead: %s" % (data, ex.code, ex.read()))
        
    def discordEmbeddedPush(self, embed):
        
        data = json.dumps({"embeds": [embed]})
        req = urllib2.Request(self._discordWebhookUrl, data, {
            'Content-Type': 'application/json',
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36"
        })
        try:
            urllib2.urlopen(req)
        except urllib2.HTTPError as ex:
            self.debug("Cannot push data to Discord. is your webhook url right?")
            self.debug("Data: %s\nCode: %s\nRead: %s" % (data, ex.code, ex.read()))